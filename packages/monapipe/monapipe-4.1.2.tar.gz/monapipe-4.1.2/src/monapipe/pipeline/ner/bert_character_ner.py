# SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

import gc
from itertools import chain
from typing import Any, List, Tuple

import numpy as np
import torch
from more_itertools import constrained_batches
from spacy.language import Language
from spacy.tokens import Doc
from transformers import AutoModelForTokenClassification, AutoTokenizer

from monapipe.config import HUGGINGFACE_HUB, SETTINGS
from monapipe.pipeline.ner.methods import create_ents_from_token_bio

from .ner import Ner


@Language.factory(
    "bert_character_ner", assigns=Ner.assigns, default_config={"set_ents_mode": "reset"}
)
def bert_character_ner(nlp: Language, name: str, set_ents_mode: str) -> Any:
    """Spacy component implementation.

    Args:
        nlp: Spacy object.
        name: Component name.
        set_ents_mode: Specifies how the new entities should be added w.r.t. existing entities in `doc.ents`.
            - "r" or "reset": The new entities overwrite the existing entities.
            - "s" or "substitute": The new entities substitute existing entities of the same label(s). Existing entities with other labels remain unchanged.
            - "u" or "unify": The new entities are unified with the existing entities.

    Returns:
        `BertCharacterNer`.
    """
    return BertCharacterNer(nlp, set_ents_mode)


class BertCharacterNer(Ner):
    """The class `BertCharacterNer`."""

    def __init__(self, nlp: Language, set_ents_mode: str):
        super().__init__(nlp, set_ents_mode)
        self.device = SETTINGS["torch_device"]
        self.model = AutoModelForTokenClassification.from_pretrained(
            **HUGGINGFACE_HUB["fiction-gbert-char-ner"]
        )
        self.id2label = {v: k for k, v in self.model.config.label2id.items()}
        self.tokenizer = AutoTokenizer.from_pretrained(**HUGGINGFACE_HUB["fiction-gbert-char-ner"])

    def idle(self):
        """
        Moves model to CPU after run.
        """
        if str(self.model.device).startswith("cuda"):
            self.model.to("cpu")
            torch.cuda.empty_cache()
            gc.collect()

    def wake_up(self):
        """
        Puts model on run-device
        """
        if str(self.model.device) != self.device:
            try:
                self.model.to(self.device)
            except RuntimeError:
                self.model.to("cpu")

    def __call__(self, doc: Doc) -> Doc:
        self.wake_up()
        token_bio = self.forward(doc)
        create_ents_from_token_bio(doc, token_bio, self.set_ents_mode)
        self.idle()
        return doc

    def forward(self, doc: Doc):
        """Tags literary characters in the document.

        Args:
            doc (Doc): Spacy doc
        """
        token_bio = {}
        chunks = self.chunk_doc(doc)
        for chunk in chunks:
            # Prepare data to align predictions with doc
            tokens, global_ids = list(zip(*chunk))

            # Get predictions
            inputs = self.tokenizer(tokens, is_split_into_words=True, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**inputs.to(self.model.device))
                logits = outputs["logits"].view(-1, 3).cpu().numpy()

            # Aggregate subword-token logits to word-level and annotate tokens in doc
            word_ids = np.array([i if i is not None else -100 for i in inputs.word_ids()])
            for word_id in set(word_ids.tolist()):
                if word_id == -100:
                    continue

                # Average decoding
                # final_logits = logits[word_id == word_ids].reshape(-1, 3).mean(axis=0)

                # Max decoding
                # final_logits = logits[word_id == word_ids].reshape(-1, 3).max(axis=0)

                # First subword representative decoding
                final_logits = logits[word_id == word_ids].reshape(-1, 3)[0, :]

                prediction = self.id2label[final_logits.argmax().item()]
                global_id = global_ids[word_id]
                token_bio[global_id] = prediction
        return token_bio

    @staticmethod
    def split_doc(doc: Doc) -> List[List[Tuple[str, int]]]:
        """Splits the content of sentences and tokens.
        Tokens are globally enumerated

        Args:
            doc (Doc): Doc to split

        Returns:
            List[List[Tuple[str, int]]]: List containing a sublist for each sentence; each sentence contains tuples of words and their global_ids.
        """
        word_idx = 0
        splitted = []
        for s in doc.sents:
            sent = []
            for t in s:
                sent.append((t.text, word_idx))
                word_idx += 1
            splitted.append(sent)
        return splitted

    def chunk_doc(self, doc: Doc) -> Tuple[List[float], List[int]]:
        """Segment a doc into segments

        Args:
            doc (Doc): _description_

        Returns:
            Tuple[List[float], List[int]]: _description_
        """
        # Tokenize complete document and assign word ids
        sentences = self.split_doc(doc)

        # Batch while respecting sentence boundaries
        def batch_length(sentence):
            s = [t[0] for t in sentence]
            return len(self.tokenizer(s, is_split_into_words=True)["input_ids"])

        batches = constrained_batches(
            sentences, max_size=self.tokenizer.model_max_length, get_len=batch_length
        )

        batches = [list(chain(*sentences)) for sentences in batches]
        return batches
