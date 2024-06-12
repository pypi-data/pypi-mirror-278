from typing import Literal
from .base_component import BaseComponent

TitleStyle = Literal[
    "blue",
    "wathet",
    "turquoise",
    "green",
    "yellow",
    "orange",
    "red",
    "carmine",
    "violet",
    "purple",
    "grey",
    "default",
]


class Title(BaseComponent):
    name: str = "title"

    def __init__(self, style: TitleStyle, children: str):
        self.props['style'] = style
        self.props['children'] = children

    def validate_props(self) -> str:
        if not self.props['children']:
            return "children is required"
        return ''
