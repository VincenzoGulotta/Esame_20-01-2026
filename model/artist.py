from dataclasses import dataclass

@dataclass
class Artist:
    id : int
    name : str
    minuti_max = float

    def __str__(self):
        return f"{self.id}, {self.name}"

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"{self.id}, {self.name}"