# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search Marc21 schema."""


from invenio_records_marc21.resources.serializers.dublin_core.schema import (
    DublinCoreSchema,
)


class Marc21RecordSchema(DublinCoreSchema):
    """Marc21RecordsSerializer."""
