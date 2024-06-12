# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# invenio-records-global-search is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Configs."""

from invenio_i18n import gettext as _

from .services.facets import data_model, formats, publishers, rights, subjects, types

GLOBAL_SEARCH_FACETS = {
    "data_model": {
        "facet": data_model,
        "ui": {
            "field": "original.schema",
        },
    },
    "subjects": {
        "facet": subjects,
        "ui": {
            "field": "metadata.subjects",
        },
    },
    "publishers": {
        "facet": publishers,
        "ui": {
            "field": "metadata.publishers",
        },
    },
    "formats": {
        "facet": formats,
        "ui": {
            "field": "metadata.formats",
        },
    },
    "rights": {
        "facet": rights,
        "ui": {
            "field": "metadata.rights",
        },
    },
    "types": {
        "facet": types,
        "ui": {
            "field": "metadata.types",
        },
    },
}

GLOBAL_SEARCH_SORT_OPTIONS = {
    "bestmatch": {
        "title": _("Best match"),
        "fields": ["_score"],  # search defaults to desc on `_score` field
    },
    "newest": {
        "title": _("Newest"),
        "fields": ["-created"],
    },
}

GLOBAL_SEARCH_SEARCH = {
    "facets": ["data_model", "subjects", "publishers", "formats", "rights", "types"],
    "sort": [
        "bestmatch",
        "newest",
    ],
}

GLOBAL_SEARCH_BASE_TEMPLATE = "invenio_records_global_search/base.html"

GLOBAL_SEARCH_ORIGINAL_SCHEMAS = {}
"""Configure the original schema names."""
