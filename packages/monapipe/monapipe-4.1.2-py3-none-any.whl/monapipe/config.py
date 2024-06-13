# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

import os

from torch import cuda

DATAVERSE = {
    "api_token": "",
    "doi_attribution": "doi:10.25625/2D9CAV&version=1.0",
    "doi_event_classification": "doi:10.25625/0GUOMC&version=1.1",
    "doi_flair_gen_tagger_cv": "doi:10.25625/V7HTB8&version=2.1",
    "doi_generalizing_passages_identification_bert": "doi:10.25625/2PHXNC&version=1.1",
    "doi_heideltime": "doi:10.25625/SIPQEF&version=1.0",
    "doi_open_multilingual_wordnet": "doi:10.25625/LE57DV&version=1.0",
    "doi_parsing": "doi:10.25625/S2LPJP&version=1.1",
    "doi_reflective_passages_identification_bert": "doi:10.25625/0HXWYG&version=1.1",
}

HUGGINGFACE_HUB = {
    "fiction-gbert-char-ner": {
        "pretrained_model_name_or_path": "LennartKeller/fiction-gbert-large-droc-np-ner",
        "revision": "a75cf9fe8be4e45856049c289a0317c82f68c50a",
    }
}

LOCAL_PATHS = {"germanet": os.path.join(os.path.dirname(__file__), "..", "..", "..", "germanet")}

SETTINGS = {
    "spacy_max_length": 12000000,
    "torch_device": ("cuda" if cuda.is_available() else "cpu"),
}
