# SPDX-FileCopyrightText: 2024 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

import os
import sys

import flair
import flair.samplers
import torch
from flair.models import SequenceTagger

from monapipe.config import SETTINGS
from monapipe.resource_handler import ResourceHandler

PATH = os.path.dirname(__file__)

RESOURCE_HANDLER = ResourceHandler(PATH)


def load() -> SequenceTagger:
    """Loading method of the `flair_gen_tagger_cv` resource.

    Returns:
        The multi-class model.

    """
    flair.device = torch.device(SETTINGS["torch_device"])
    sys.modules["imbalanced_sampler"] = flair.samplers
    return SequenceTagger.load(os.path.join(PATH, "multi_100_mixed1_5", "final-model.pt"))
