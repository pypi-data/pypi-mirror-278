from typing import Optional, Dict
from .base_component import BaseComponent


class Chart(BaseComponent):
    name: str = "chart"

    def __init__(self, chartSpec: Dict, options: Optional[Dict] = None):
        self.props['chartSpec'] = chartSpec
        self.props['options'] = options
