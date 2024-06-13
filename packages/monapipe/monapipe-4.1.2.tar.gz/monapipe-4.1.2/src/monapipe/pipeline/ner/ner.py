# SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from spacy.language import Language


class Ner:
    assigns = {"doc.ents"}

    def __init__(self, nlp: Language, set_ents_mode: str) -> None:
        self.set_ents_mode = set_ents_mode
