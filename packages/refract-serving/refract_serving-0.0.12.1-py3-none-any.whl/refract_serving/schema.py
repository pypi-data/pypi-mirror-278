# -*- coding: utf-8 -*-
"""Schemas for mosaic ai backend views"""
from marshmallow import fields, schema


# pylint: disable=too-few-public-methods
class SchemaMixin:
    """Schema mixin class"""

    id = fields.Str()
    created_by = fields.Str()
    created_on = fields.DateTime(dump_only=True)
    last_modified_by = fields.Str()
    last_modified_on = fields.DateTime(dump_only=True)


class MLModelRequestLogSchema(schema.Schema, SchemaMixin):
    """Schema for ML model request log """

    request_id = fields.Str()
    model_id = fields.Str(
        required=True, error_messages={"required": "ml_model_id is required"}
    )
    version_id = fields.Str(
        required=True, error_messages={"required": "version_id is required"}
    )
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    status = fields.Str()
    feedback = fields.Str()
    metric_value = fields.Dict()


class FeedbackSchema(schema.Schema):
    request_id = fields.Str(
        required=True, error_messages={"required": "Request id is required"}
    )
    feedback = fields.Str(
        required=True, error_messages={"required": " feedback is required"}
    )
