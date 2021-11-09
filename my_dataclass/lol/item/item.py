from dataclasses import dataclass, field, asdict
from typing import Dict, Any


@dataclass
class Item:
    name: str
    id: int
    hp: float = field(default=0)
    gold: int = field(default=0)
    hpregen: float = field(default=0)
    armor: float = field(default=0)
    ad: float = field(default=0)
    ap: float = field(default=0)
    mr: float = field(default=0)
    movespeed: float = field(default=0)
    movespeedpercent: float = field(default=0)
    attackspeedpercent: float = field(default=0)
    crit: float = field(default=0)
    lifestealpercent: float = field(default=0)
    armorpen: float = field(default=0)
    armorpenpercent: float = field(default=0)
    magicpenpercent: float = field(default=0)
    magicpen: float = field(default=0)
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
