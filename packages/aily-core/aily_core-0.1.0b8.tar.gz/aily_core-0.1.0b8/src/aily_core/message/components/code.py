from .base_component import BaseComponent


class Code(BaseComponent):
    def __init__(self, children: str) -> None:
        self.props['children'] = children

    def validate_props(self) -> str:
        if not self.props['children']:
            return "children is required"

    def to_message(self) -> str:
        return f"```{self.props['children']}```"
