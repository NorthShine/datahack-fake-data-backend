from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from dataclasses import make_dataclass

from no_spark_in_my_home.src.generator import FakeDataGenerator


class ForeignKey(BaseModel):
    field: str
    foreignField: str


class FakeSQLField(BaseModel):
    name: str
    type: str


class FakeSQLModel(BaseModel):
    fields: List[FakeSQLField] = []
    foreignKeys: Optional[List[ForeignKey]] = None
    m2mFields: Optional[List[ForeignKey]] = None
    whereClauses: Optional[str] = None


class Dataclass(BaseModel):
    name: str
    sqlModel: FakeSQLModel


DEFAULT_TYPES_TRANSLATION = {
    "string": "str"
}


app = FastAPI()


@app.post('/generate_sql')
async def hello(fields: Dataclass):
    sqlModel = fields.sqlModel
    fields_enumeration = []
    for name, type in sqlModel.fields:
        translated_type = DEFAULT_TYPES_TRANSLATION.get(type[1], type[1])
        fields_enumeration.append((name[1], translated_type))
    dataclass = make_dataclass(fields.name, fields_enumeration)
    generator = FakeDataGenerator(dataclass)
    data = generator.load()
    return data
