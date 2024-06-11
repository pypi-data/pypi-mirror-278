# -*- coding: utf-8 -*-
import logging
from mosaicml_serving.constants import Database
from sqlalchemy import create_engine, pool
import os
from sqlalchemy.orm import sessionmaker

log = logging.getLogger("mosaic-ai-backend")
log.setLevel(logging.DEBUG)


def create_db_connection():
    """creates database connection"""
    log.info("Creating database session")
    db_engine = create_db_engine()
    db_session = create_db_session(db_engine)
    log.info("Session created successfully")
    return db_session


def create_db_session(db_engine):
    """Creates database session"""
    session_maker = sessionmaker(bind=db_engine)
    return session_maker()


def close_db_connection(db_session):
    """function to close database connections"""
    db_session.close()
    log.info("Session closed successfully")
    return None


def create_db_engine():
    """Creates DB engine"""
    db_url = os.getenv(
        Database.url, "mysql+mysqlconnector://root:root@localhost/ai_logistics"
    )
    return create_engine(db_url, poolclass=pool.NullPool)
