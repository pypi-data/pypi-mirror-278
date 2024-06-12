from .base_component import BaseComponent


class ItemList(BaseComponent):

    def __init__(self, items: list[str]):
        self.props['items'] = items

    def to_message(self) -> str:
        if not self.props['items']:
            raise "image, validate err: items is required"

        return "\n".join(f"- {item}" for item in self.props['items'])
