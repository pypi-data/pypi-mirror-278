from typing import List
import json


class BaseComponent:

    children_wrapper: str = ''

    @property
    def props(self):
        if not hasattr(self, '_props'):
            self._props = {}
        return self._props

    def validate_props(self) -> str:
        return ''

    def prop_lines(self) -> List[str]:
        lines = []
        for key, value in self.props.items():
            if key == 'children' or value is None:
                continue
            if isinstance(value, str):
                lines.append(f"{key}='{value}'")
            else:
                lines.append(f"{key}={json.dumps(value, indent=2)}")
        return lines

    def prop_lines_string(self) -> str:
        lines = self.prop_lines()
        if len(lines) == 0:
            return ""
        return f" {' '.join(lines)}"

    def to_message(self) -> str:
        if not self.name:
            return ""

        err = self.validate_props()
        if err:
            raise Exception(err)

        if "children" in self.props:
            children = self.props["children"]
            children_message = ""
            if isinstance(children, list):
                children_message = "\n".join(
                    child.to_message()
                    if isinstance(child, BaseComponent) else str(child)
                    for child in children
                )
            elif isinstance(children, BaseComponent):
                children_message = children.to_message()
            else:
                children_message = str(children)

            return "".join([
                f"<{self.name}{self.prop_lines_string()}>",
                self.children_wrapper, children_message, self.children_wrapper,
                f"</{self.name}>",
            ])
        else:
            return f"<{self.name}{self.prop_lines_string()} />"
