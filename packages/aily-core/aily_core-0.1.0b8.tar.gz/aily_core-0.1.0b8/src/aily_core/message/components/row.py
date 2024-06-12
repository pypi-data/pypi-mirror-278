from .base_component import BaseComponent


class Row(BaseComponent):
    name: str = "row"

    def __init__(self, children: list[BaseComponent]):
        self.props['children'] = children

    def validate_props(self) -> str:
        if not self.props['children']:
            return "children is required"
        return ''
