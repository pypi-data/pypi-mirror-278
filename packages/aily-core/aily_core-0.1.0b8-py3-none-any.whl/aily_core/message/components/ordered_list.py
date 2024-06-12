from .base_component import BaseComponent


class OrderedList(BaseComponent):
    def __init__(self, items: list[str]):
        self.props['items'] = items

    def validate_props(self) -> str:
        if not self.props['items']:
            return "items is required"
        return ''

    def to_message(self) -> str:
        err = self.validate_props()
        if err:
            raise err

        return "\n".join(f"{idx + 1}. {item}" for idx, item in enumerate(self.props['items']))
