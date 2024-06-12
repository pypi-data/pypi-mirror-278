# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2024 Graz University of Technology.
#
# invenio-records-global-search is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Global Search Record Resource schema."""

from flask import current_app
from marshmallow import Schema, fields
from marshmallow_utils.fields import SanitizedUnicode


def access_status(_: dict) -> dict:
    """Access status."""
    return {
        "id": "open",
        "icon": "unlock",
        "title_l10n": "Open",
        "description_l10n": "Open",
    }


def created_date_l10n_long(obj: dict) -> str:
    """Create date l10n long."""
    if "dates" in obj["metadata"] and len(obj["metadata"]["dates"]) > 0:
        return obj["metadata"]["dates"][0]
    return "N/A"


class OriginalSchema(Schema):
    """Original Schema."""

    view = fields.String(attribute="view")
    schema_l10n = fields.Method("get_schema_l10n")

    def get_schema_l10n(self, obj: dict) -> str:
        """Get schema l10n."""
        schemas = current_app.config.get("GLOBAL_SEARCH_ORIGINAL_SCHEMAS", {})
        for schema_name, schema in schemas.items():
            if schema_name == obj["schema"]:
                return schema["name_l10n"]
        return ""


class GlobalSearchSchema(Schema):
    """Schema for dumping extra information for the global search record."""

    id = SanitizedUnicode(data_key="id", attribute="id")

    access_status = fields.Function(access_status)

    original = fields.Nested(OriginalSchema, attribute="original")

    created_date_l10n_long = fields.Function(created_date_l10n_long)

    class Meta:
        """Meta class to accept unknwon fields."""

        additional = ("metadata",)
