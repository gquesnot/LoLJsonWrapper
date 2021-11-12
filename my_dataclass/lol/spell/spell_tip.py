from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class SpellTip:
    label: str
    effect: str

    @classmethod
    def from_dict(cls, dc, data: Dict[str, Any]) -> "SpellTip":
        # data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
