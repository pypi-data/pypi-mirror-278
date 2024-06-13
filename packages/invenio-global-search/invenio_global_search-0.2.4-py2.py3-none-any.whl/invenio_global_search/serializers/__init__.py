# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Serializers."""

from .lom import LOMRecordJSONSerializer
from .marc21 import Marc21RecordJSONSerializer
from .rdm import RDMRecordJSONSerializer

__all__ = (
    "RDMRecordJSONSerializer",
    "Marc21RecordJSONSerializer",
    "LOMRecordJSONSerializer",
)
