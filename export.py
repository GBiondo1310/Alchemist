from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, union_all
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Query, sessionmaker
from sqlalchemy.engine import create_engine


# ===== DATABASE SETUP ===== #

engine = create_engine("sqlite:///.sqlite", echo=True)
Session = sessionmaker(engine)
session = Session()
Base = declarative_base(engine)

# ===== DATABASE SETUP ===== #