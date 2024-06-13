# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2024 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search Marc21 serializer."""

from flask_resources import BaseListSchema, MarshmallowSerializer
from flask_resources.serializers import JSONSerializer

from .schema import Marc21RecordSchema


class Marc21RecordJSONSerializer(MarshmallowSerializer):
    """Marshmallow based DataCite serializer for records."""

    def __init__(self, **kwargs: dict) -> None:
        """Construct."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=Marc21RecordSchema,
            list_schema_cls=BaseListSchema,
            **kwargs,
        )
