from typing import List, Union
from .base_component import BaseComponent


class Note(BaseComponent):
    name: str = "record"

    def __init__(self, children: Union[BaseComponent, List[BaseComponent], str]):
        self.props['children'] = children

    def validate_props(self) -> str:
        if not self.props['children']:
            return "children is required"
        return ''
