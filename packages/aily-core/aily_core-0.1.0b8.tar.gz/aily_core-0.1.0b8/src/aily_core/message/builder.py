from typing import List, Mapping, Union

from .components.base_component import BaseComponent

LineType = Union[BaseComponent, str]


class MessageBuilderOptions:
    def __init__(self, line_divider: str = "\n"):
        self.line_divider = line_divider


class MessageBuilder:
    def __init__(self, options: Mapping[str, str] = {}):
        self.lines: List[LineType] = []
        self.options = MessageBuilderOptions(**options)

    def add_line(self, component: LineType):
        self.lines.append(component)
        return self

    def to_message(self) -> str:
        return self.options.line_divider.join(
            line.to_message()
            if isinstance(line, BaseComponent) else str(line)
            for line in self.lines
        )
