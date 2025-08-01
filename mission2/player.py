
from dataclasses import dataclass
from typing import List
from mission2.grade import Grade
from mission2.config import config

@dataclass
class Player:
    id: int
    name: str
    attendance_count: List[int]
    points: int = 0
    grade: Grade = 0

    def __init__(self, id: int, name: str):
        super().__init__()
        self.id = id
        self.name = name
        self.attendance_count = [0] * len(config.DAY_INDEX)

    @property
    def attendance_count_on_wednesday(self) -> int:
        return self.attendance_count[config.WEDNESDAY]

    @property
    def attendance_count_on_weekend(self) -> int:
        return self.attendance_count[config.SATURDAY] + self.attendance_count[config.SUNDAY]
