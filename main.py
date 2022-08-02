from typing import Dict, List, Optional
from fastapi import FastAPI
from pydantic import BaseModel


class ForeignKey(BaseModel):
    field: str
    foreignField: str


class WhereClause(BaseModel):
    field: str
    whereExpression: str


class FakeSQLField(BaseModel):
    name: str
    type: str
    foreignKeys: Optional[List[ForeignKey]] = None
    m2mFields: Optional[List[ForeignKey]] = None
    whereClauses: Optional[List[WhereClause]] = None


class FakeSQLModel(BaseModel):
    fields: List[FakeSQLField] = []


class Dataclass(BaseModel):
    sqlModel: FakeSQLModel


app = FastAPI()


@app.post('/generate_sql')
async def hello(fields: Dataclass):
    return "Hello"
