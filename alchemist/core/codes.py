IMPORTS = """from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, union_all
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Query, sessionmaker
from sqlalchemy.engine import create_engine


# ===== DATABASE SETUP ===== #

engine = create_engine("sqlite:///%database_name%.sqlite", echo=True)
Session = sessionmaker(engine)
session = Session()
Base = declarative_base(engine)

# ===== DATABASE SETUP ===== #"""

CLASS_BASE = """
class %classname%(Base):
    __tablename__="%tablename%"
    id: int = Column(Integer, primary_key = True)
"""

# Fields

DATETIME = """
    %fieldname%: datetime = Column(DateTime, deatult = datetime.now())"""

INT = """
    %fieldname%: int = Column(Integer)"""

FLOAT = """
    %fieldname%: float = Column(Float)"""

STRING = """
    %fieldname%: string = Column(String)"""

BOOL = """
%fieldname%: bool = Column(Boolean)"""

RELATIONSHIP_PARENT = """
    %child_tablename%: list[%child_class%] = relationship("%child_class%", back_populates="%parent_tablename%")"""

RELATIONSHIP_CHILD_FK = """
    %parent_tablename%: int = Column(Integer, ForeignKey("%parent_tablename%.id"))"""

RELATIONSHIP_CHILD = """
    %parent_tablename%: %parent_class%= relationship("%parent_class%", back_populates="%child_tablename%s")
    """
