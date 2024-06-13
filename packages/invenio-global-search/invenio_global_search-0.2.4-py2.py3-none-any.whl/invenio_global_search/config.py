# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search Configs."""

from invenio_i18n import gettext as _

from .cli import rebuild_database_lom, rebuild_database_marc21, rebuild_database_rdm

GLOBAL_SEARCH_ORIGINAL_SCHEMAS = {
    "lom": {
        "schema": "lom",
        "name_l10n": _("OER"),
    },
    "rdm": {
        "schema": "rdm",
        "name_l10n": _("Research Result"),
    },
    "marc21": {
        "schema": "marc21",
        "name_l10n": _("Publication"),
    },
}

GLOBAL_SEARCH_REBUILD_DATABASE = [
    rebuild_database_rdm,
    rebuild_database_marc21,
    rebuild_database_lom,
]
