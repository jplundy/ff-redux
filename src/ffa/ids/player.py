from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerID:
    """Simple identifier for a player."""

    name: str
    position: str
    team: str

    @classmethod
    def from_row(cls, row: dict) -> "PlayerID":
        """Create a :class:`PlayerID` from a mapping.

        The mapping is expected to have at least the keys ``Name``,
        ``_position`` (or ``Position``) and ``_team`` (or ``Team``).
        """

        name = row.get("Name") or row.get("Player")
        position = row.get("_position") or row.get("Position")
        team = row.get("_team") or row.get("Team")
        return cls(name=name, position=position, team=team)

    def as_tuple(self) -> tuple[str, str, str]:
        return (self.name, self.position, self.team)
