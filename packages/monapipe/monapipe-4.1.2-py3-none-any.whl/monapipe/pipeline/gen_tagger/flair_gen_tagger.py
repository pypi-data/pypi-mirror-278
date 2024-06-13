# SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from typing import Any, Dict, Set

import transformers
from flair.data import Sentence
from flair.models import SequenceTagger
from spacy.language import Language
from spacy.tokens import Doc, Span

import monapipe.resource_handler as resources
from monapipe.pipeline.gen_tagger.gen_tagger import GenTagger
from monapipe.pipeline.methods import requires, update_token_span_groups
from monapipe.pipeline.reflection_tagger.methods import create_passages_from_clause_tags


@Language.factory(
    "flair_gen_tagger",
    assigns=GenTagger.assigns,
    default_config={"label_condition": "multi"},
)
def flair_gen_tagger(nlp: Language, name: str, label_condition: str) -> Any:
    """Spacy component implementation.
        Add generalising passages to the document.
        Uses the code and the multi-class model from here:
        https://gitlab.gwdg.de/tillmann.doenicke/thesis

    Args:
        nlp: Spacy object.
        name: Component name.
        label_condition: Label condition ("multi" or "binary").

    Returns:
        `FlairGenTagger`.

    """
    return FlairGenTagger(nlp, label_condition)


class FlairGenTagger(GenTagger):
    """The class `FlairGenTagger`."""

    def __init__(self, nlp: Language, label_condition: str):
        requires(self, nlp, ["clausizer"])

        if label_condition not in ["binary", "multi"]:
            raise ValueError('Label condition must be "binary" or "multi".')

        super().__init__(nlp, label_condition)

    def __call__(self, doc: Doc) -> Doc:
        model = resources.access("flair_gen_tagger_cv")

        all_clause_labels = {}

        chunks = []
        chunk = []
        for sent in doc.sents:
            tokens = list(sent)
            if len(chunk) + len(tokens) <= 100 or len(chunk) == 0:
                chunk.extend(tokens)
            else:
                chunks.append(chunk)
                chunk = tokens
        if len(chunk) > 0:
            chunks.append(chunk)
        for chunk in chunks:
            text = " ".join([token.text for token in chunk if not token.is_space])
            text = Sentence(text, use_tokenizer=False)
            clause_labels = self.get_clause_labels(chunk, text, model)
            for clause in clause_labels:
                all_clause_labels[clause] = clause_labels[clause]
        
        if self.label_condition == "binary":
            for clause in all_clause_labels:
                if len(all_clause_labels[clause]) > 0:
                    all_clause_labels[clause].clear()
                    all_clause_labels[clause].add("GI")

        labels = []
        for clause in doc._.clauses:
            try:
                labels.append(all_clause_labels[clause])
            except KeyError:
                labels.append(set())

        create_passages_from_clause_tags(doc, "gi", labels)

        update_token_span_groups(doc, ["gi"])

        return doc

    def get_clause_labels(
        self, sent: Span, text: Sentence, tagger: SequenceTagger
    ) -> Dict[Span, Set[str]]:
        """Get the labels for each clause in a sentence.

        Args:
            sent: The sentence in spacy format.
            text: The sentence in flair format.
            tagger: The flair tagger model.

        Returns:
            A dictionary that maps clauses to labels.

        """
        try:
            try:
                tagger.predict(text)
            except AttributeError:
                # The `flair` models were trained with an earlier version of `transformers`,
                # where some attributes did not exist that are now expected.
                # These attributes are set here:
                transformers.models.bert.tokenization_bert.BasicTokenizer.do_split_on_punc = True
                transformers.models.bert.tokenization_bert.BertTokenizer._added_tokens_encoder = {}
                transformers.tokenization_utils.PreTrainedTokenizer.split_special_tokens = False
                tagger.predict(text)
            clause_tags = {token._.clause: {} for token in sent if token._.clause is not None}
            s = 0
            for i, token in enumerate(sent):
                if token.is_space:
                    s += 1
                else:
                    tag = text.tokens[i - s].get_labels()[0].value
                    if tag != "-":
                        if token._.clause is not None:
                            if tag not in clause_tags[token._.clause]:
                                clause_tags[token._.clause][tag] = 0
                            clause_tags[token._.clause][tag] += 1
            for clause in clause_tags:
                clause_tags[clause] = set(
                    [
                        tag
                        for tag in clause_tags[clause]
                        if 1.0 * clause_tags[clause][tag] / len(clause._.tokens) >= 0.5
                    ]
                )
            return clause_tags
        except RuntimeError:  # input sequence too long
            return {token._.clause: set() for token in sent if token._.clause is not None}
