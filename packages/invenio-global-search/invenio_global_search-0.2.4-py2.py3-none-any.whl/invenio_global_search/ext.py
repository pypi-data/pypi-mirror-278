# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2024 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search for InvenioRDM."""


from flask import Flask

from . import config


class InvenioGlobalSearch:
    """InvenioGlobalSearch."""

    def __init__(self, app: Flask) -> None:
        """Construct InvenioGlobalSearch."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-global-search"] = self

    @staticmethod
    def init_config(app: Flask) -> None:
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("GLOBAL_SEARCH_"):
                app.config.setdefault(k, getattr(config, k))
