from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    lang: Optional[str] = None
    limit: Optional[int] = None
    mask_per_field: Optional[dict] = None
    maxlength_per_field: Optional[List[dict]] = None
    range_per_field: Optional[dict] = None


class Dataclasses(BaseModel):
    models: List[Dataclass]


DEFAULT_TYPES_TRANSLATION = {
    "string": "str"
}


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post('/generate_sql')
async def hello(dataclasses: Dataclasses):
    dataclasses_data = []
    for fields in dataclasses.models:
        sqlModel = fields.sqlModel
        fields_enumeration = []
        for name, type in sqlModel.fields:
            translated_type = DEFAULT_TYPES_TRANSLATION.get(type[1], type[1])
            fields_enumeration.append((name[1], translated_type))
        dataclass = make_dataclass(fields.name, fields_enumeration)
        generator = FakeDataGenerator(
            dataclass,
            limit=fields.limit,
            lang=fields.lang,
            mask_per_field=fields.mask_per_field,
            range_per_field=fields.range_per_field,
            maxlength_per_field=fields.maxlength_per_field,
        )
        data = generator.load(as_dicts=True)
        dataclasses_data.append({"name": fields.name, "data": data})
    return dataclasses_data
