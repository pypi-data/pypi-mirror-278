from typing import Union
from .base_component import BaseComponent


class Highlight(BaseComponent):
    children_wrapper: str = '\n'
    name: str = "highlight"

    def __init__(self, children: Union[str, list[str]]):
        self.props['children'] = children

    def validate_props(self) -> str:
        if not self.props['children']:
            return "children is required"
        return ''
