# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search for InvenioRDM."""

from .components import (
    LOMToGlobalSearchComponent,
    Marc21ToGlobalSearchComponent,
    RDMToGlobalSearchComponent,
)
from .ext import InvenioGlobalSearch

__version__ = "0.2.4"

__all__ = (
    "__version__",
    "InvenioGlobalSearch",
    "LOMToGlobalSearchComponent",
    "Marc21ToGlobalSearchComponent",
    "RDMToGlobalSearchComponent",
)
