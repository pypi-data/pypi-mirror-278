from typing import Literal, Optional, Union
from .base_component import BaseComponent

ButtonType = Literal[
    "default",
    "primary",
    "danger",
    "text",
    "primaryFilled",
    "dangerFilled",
    "primaryText",
    "dangerText"
]

ButtonSize = Literal["tiny", "small", "medium", "large"]

ButtonUrlMode = Literal["default", "raw"]


class Button(BaseComponent):
    name = "button"

    def validate_props(self) -> str:
        if not self.props['action']:
            return "action is required"
        if self.props['action'] == 'navigate' and not self.props['url']:
            return "url is required when action is navigate"
        return ''

    def __init__(self,
                 children: str,
                 action: Optional[Literal["navigate", "message"]],
                 url: str = None,
                 type: Optional[ButtonType] = None,
                 width: Optional[Union[Literal["default",
                                               "fill"], str]] = None,
                 size: Optional[ButtonSize] = None,
                 urlMode: Optional[ButtonUrlMode] = None,
                 message: Optional[str] = None,
                 skill: Optional[str] = None,
                 ):
        self.props['children'] = children
        self.props['url'] = url
        self.props['action'] = action
        self.props['type'] = type
        self.props['width'] = width
        self.props['size'] = size
        self.props['urlMode'] = urlMode
        self.props['message'] = message
        self.props['skill'] = skill
