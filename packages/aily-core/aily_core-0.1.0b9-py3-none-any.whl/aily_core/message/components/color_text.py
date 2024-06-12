from .base_component import BaseComponent


class ColorText(BaseComponent):
    name: str = "font"

    def __init__(self, children: str, color: str):
        self.props['children'] = children
        self.props['color'] = color

    def validate_props(self) -> str:
        if not self.props['children']:
            return "children is required"
        if not self.props['color']:
            return "color is required"
        return ''
