from typing import Literal
from .base_component import BaseComponent

TableColumnType = Literal[
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


class TableColumn():
    type: TableColumnType
    name: str
    displayName: str
    width: str

    def __init__(self, type: TableColumnType, name: str, displayName: str, width: str):
        self.type = type
        self.name = name
        self.displayName = displayName
        self.width = width


class Table(BaseComponent):
    name: str = "table"

    def __init__(self, columns: list[TableColumn], data: list[dict], pageSize: int, rowHeight: str):
        self.props['columns'] = columns
        self.props['data'] = data
        self.props['pageSize'] = pageSize
        self.props['rowHeight'] = rowHeight

    def validate_props(self) -> str:
        if not self.props['columns']:
            return "columns is required"
        if not self.props['data']:
            return "data is required"
        return ''
