# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2024 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Components to Hook into other data models."""

from collections.abc import Callable

from flask import current_app
from flask_principal import Identity
from flask_resources import MarshmallowSerializer
from invenio_rdm_records.records.api import RDMDraft, RDMRecord
from invenio_rdm_records.resources.serializers.dublincore import (
    DublinCoreJSONSerializer,
)
from invenio_records.api import Record
from invenio_records_global_search import current_records_global_search
from invenio_records_lom.records import LOMRecord
from invenio_records_lom.utils import LOMMetadata
from invenio_records_marc21.records import Marc21Record
from invenio_records_marc21.services.record import Marc21Metadata
from invenio_records_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.uow import Operation, UnitOfWork
from marshmallow.exceptions import ValidationError

from .serializers import LOMRecordJSONSerializer, Marc21RecordJSONSerializer


def map_metadata_from_a_to_b(
    record: Record,
    serializer_cls: MarshmallowSerializer = None,
    metadata_cls: Marc21Metadata | LOMMetadata | None = None,
    schema: str | None = None,
    identity: Identity = None,
) -> None:
    """Func."""
    schema_mapping = {
        "rdm": "records",
        "lom": "oer",
        "marc21": "publications",
    }

    record_serializer = serializer_cls()
    data = record.dumps()

    if data["access"]["record"] != "public":
        return

    obj = metadata_cls(json=data["metadata"]) if metadata_cls else data
    metadata = record_serializer.dump_obj(obj)
    pid = record["id"]
    path = schema_mapping[schema]
    original = {
        "view": f"{path}/{pid}",
        "schema": schema,
        "pid": pid,
    }
    data = {
        "metadata": metadata,
        "original": original,
    }

    try:
        current_records_global_search.records_service.create_or_update(
            identity=identity,
            data=data,
        )
    except ValidationError as error:
        msg = "GLOBAL SEARCH pid: %s has following validation error: %s"
        current_app.logger.warning(msg, pid, error)


class ComponentOp(Operation):
    """ComponentOp."""

    def __init__(
        self,
        record: Record,
        func: Callable = map_metadata_from_a_to_b,
        serializer_cls: MarshmallowSerializer = None,
        metadata_cls: Marc21Metadata | LOMMetadata | None = None,
        schema: str | None = None,
        identity: Identity = None,
    ) -> None:
        """Construct."""
        self._record = record
        self._func = func
        self._serializer_cls = serializer_cls
        self._metadata_cls = metadata_cls
        self._schema = schema
        self._identity = identity

    def on_post_commit(self, _: UnitOfWork) -> None:
        """Post commit."""
        self._func(
            self._record,
            self._serializer_cls,
            self._metadata_cls,
            self._schema,
            self._identity,
        )


class Marc21ToGlobalSearchComponent(ServiceComponent):
    """Marc21ToGlobalSearchComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: Marc21Record | None = None,
        **__: dict,
    ) -> None:
        """Create handler."""
        cmp_op = ComponentOp(
            record,
            serializer_cls=Marc21RecordJSONSerializer,
            metadata_cls=Marc21Metadata,
            schema="marc21",
            identity=identity,
        )
        self.uow.register(cmp_op)


class LOMToGlobalSearchComponent(ServiceComponent):
    """LOMToGlobalSearchComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: LOMRecord | None = None,
        **__: dict,
    ) -> None:
        """Create handler."""
        cmp_op = ComponentOp(
            record,
            serializer_cls=LOMRecordJSONSerializer,
            metadata_cls=LOMMetadata,
            schema="lom",
            identity=identity,
        )
        self.uow.register(cmp_op)


class RDMToGlobalSearchComponent(ServiceComponent):
    """RDMToGlobalSearchComponent."""

    def publish(
        self,
        identity: Identity,
        data: dict | None = None,  # noqa: ARG002
        record: RDMRecord | None = None,
        draft: RDMDraft | None = None,  # noqa: ARG002
        **__: dict,
    ) -> None:
        """Create handler."""
        cmp_op = ComponentOp(
            record,
            serializer_cls=DublinCoreJSONSerializer,
            schema="rdm",
            identity=identity,
        )
        self.uow.register(cmp_op)
