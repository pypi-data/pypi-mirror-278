# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search rdm schema."""

from invenio_rdm_records.resources.serializers.dublincore.schema import DublinCoreSchema


class RDMRecordSchema(DublinCoreSchema):
    """RDMRecordsSerializer."""
