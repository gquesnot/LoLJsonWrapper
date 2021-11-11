from dataclasses import dataclass, field, asdict
from typing import Any, Union, List, Dict
from dacite import from_dict
import keyword


@dataclass
class MatchTimeLineParticipant:
    id: int = field(default=None)
    puuid: str = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MatchTimeLineParticipant":
        data = {k if k in keyword.kwlist else f"{k}_": v for k, v in data.items()}
        return from_dict(cls, data=data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
