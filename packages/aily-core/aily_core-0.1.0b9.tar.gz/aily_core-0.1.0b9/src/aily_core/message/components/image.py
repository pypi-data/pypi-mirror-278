from .base_component import BaseComponent


class Image(BaseComponent):
    name: str = "image"

    def __init__(self, src: str, alt: str = ""):
        self.props['src'] = src
        self.props['alt'] = alt

    def validate_props(self) -> str:
        if not self.props['src']:
            return "src is required"
        return ''
