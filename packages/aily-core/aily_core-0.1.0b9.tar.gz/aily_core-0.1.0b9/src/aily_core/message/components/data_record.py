from typing import Any, Dict, List, Literal, Optional
from .base_component import BaseComponent


RecordFieldType = Literal[
    "string",
    "number",
    "boolean",
    "array",
    "object",
    "date",
    "options",
    "persons",
    "markdown",
]


class RecordField(Dict[str, Any]):
    type: RecordFieldType
    name: str
    displayName: str = ""

    def __init__(self, type: str, name: str, displayName: Optional[str]):
        self.type = type
        self.name = name
        self.displayName = displayName


class DataRecord(BaseComponent):
    name: str = "record"

    def __init__(self, fields: List[RecordField], data: Dict[str, Any]):
        self.props['fields'] = fields
        self.props['data'] = data

    def validate_props(self) -> str:
        if not self.props['fields']:
            return "fields is required"
        if not self.props['data']:
            return "data is required"
        return ''
