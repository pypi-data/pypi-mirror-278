from sqlalchemy import MetaData, Column, Integer, String
from sqlalchemy.orm import declarative_base

local_string_database_name = "lapa_testing"

local_string_schema_name = "public"

Base = declarative_base(metadata=MetaData(schema=local_string_schema_name))

data_to_insert = []


class Test(Base):
    __tablename__ = "test"

    test_id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    test_text = Column(String, nullable=False)
