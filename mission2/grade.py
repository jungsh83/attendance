from abc import ABC, abstractmethod

class Grade(ABC):
    name: str
    @abstractmethod
    def evaluate(self, points: int) -> bool:
        ...


class GoldGrade(Grade):
    def __init__(self):
        self.name = "GOLD"

    def evaluate(self, points: int) -> bool:
        if points >= 50:
            return True
        return False

class SilverGrade(Grade):
    def __init__(self):
        self.name = "SILVER"

    def evaluate(self, points: int) -> bool:
        if 30 <= points < 50:
            return True
        return False

class NormalGrade(Grade):
    def __init__(self):
        self.name = "NORMAL"

    def evaluate(self, points: int) -> bool:
        return True

class GradeFactory:
    @classmethod
    def get_grade(cls, point: int) -> Grade:
        for grade in [GoldGrade(), SilverGrade()]:
            if grade.evaluate(point):
                return grade
        return NormalGrade()