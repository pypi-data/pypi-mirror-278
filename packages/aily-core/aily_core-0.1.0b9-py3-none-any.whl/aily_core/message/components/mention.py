from .base_component import BaseComponent


class Mention(BaseComponent):
    name: str = "at"

    def __init__(self, id: str = None, email: str = None):
        self.props['id'] = id
        self.props['email'] = email

    def validate_props(self) -> str:
        if not self.props['id'] and not self.props['email']:
            return "id or email is required"
