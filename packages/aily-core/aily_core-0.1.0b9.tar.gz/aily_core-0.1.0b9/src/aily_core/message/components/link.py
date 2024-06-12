from .base_component import BaseComponent


class Link(BaseComponent):
    name: str = "link"

    def __init__(self, text: str, url: str):
        self.props['text'] = text
        self.props['url'] = url

    def validate_props(self) -> str:
        if not self.props['text']:
            return "text is required"
        if not self.props['url']:
            return "url is required"

    def to_message(self) -> str:
        err = self.validate_props()
        if err:
            raise err

        return f"[{self.props['text']}]({self.props['url']})"
