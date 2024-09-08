from langchain.pydantic_v1 import BaseModel
from typing import List

class RunQueryArgsSchema(BaseModel):
    query: str

class DescribeTablesArgsSchema(BaseModel):
    tables_names: List[str]

class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str
