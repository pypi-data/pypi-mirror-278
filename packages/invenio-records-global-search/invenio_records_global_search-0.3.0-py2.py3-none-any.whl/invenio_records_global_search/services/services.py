# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2024 Graz University of Technology.
#
# invenio-records-global-search is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Global Search Services."""

from flask_principal import Identity
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_records_resources.services import RecordService
from invenio_records_resources.services.records.results import RecordItem
from invenio_records_resources.services.uow import UnitOfWork, unit_of_work


class GlobalSearchRecordService(RecordService):
    """Global search record service."""

    @unit_of_work()
    def create_or_update(
        self,
        identity: Identity,
        data: dict,
        uow: UnitOfWork | None = None,
        *,
        expand: bool = False,
    ) -> RecordItem:
        """Create a record.

        :param identity: Identity of user creating the record.
        :param data: Input data according to the data schema.
        """
        gs_pid = "gs-" + data["original"]["pid"]

        try:
            # only to check if a exists already
            self.record_cls.pid.resolve(gs_pid)

            return self.update(identity, id_=gs_pid, data=data)
        except PIDDoesNotExistError:
            self.record_cls.gs_pid = gs_pid
            return self._create(self.record_cls, identity, data, uow=uow, expand=expand)
