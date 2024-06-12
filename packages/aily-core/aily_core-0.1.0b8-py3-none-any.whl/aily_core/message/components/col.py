from typing import Union
from .base_component import BaseComponent


class Col(BaseComponent):
    name: str = "col"

    def __init__(self, flex: int, children: Union[BaseComponent, str]):
        self.props['flex'] = flex
        self.props['children'] = children
