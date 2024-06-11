# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
from mosaicml_serving.utils import get_db_type, uuid_generator


Base = declarative_base()
# pylint: disable=invalid-name, too-few-public-methods
db_type = get_db_type()


class MLModelRequestLog(Base):
    """Model for ML model request log"""

    __tablename__ = "ml_model_request_log"
    request_id = sa.Column(
        sa.String(100), primary_key=True, nullable=False, default=uuid_generator
    )
    model_id = sa.Column(sa.String(100), nullable=False)
    version_id = sa.Column(sa.String(100), nullable=False)
    if db_type == "mysql":
        start_time = sa.Column(mysql.DATETIME(fsp=6))
        end_time = sa.Column(mysql.DATETIME(fsp=6))
    else:
        start_time = sa.Column(sa.DateTime)
        end_time = sa.Column(sa.DateTime)
    status = sa.Column(sa.String(100))
    feedback = sa.Column(sa.String(20))
    metric_value = sa.Column(sa.JSON)
