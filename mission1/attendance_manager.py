from pathlib import Path
from typing import List, Dict

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = (i for i in range(7))
DAY_INDEX = {"monday": MONDAY, "tuesday": TUESDAY, "wednesday": WEDNESDAY, "thursday": THURSDAY, "friday": FRIDAY, "saturday": SATURDAY, "sunday": SUNDAY}
NORMAL, GOLD, SILVER = (i for i in range(3))
GRADE_NAME = {0: "NORMAL", 1: "GOLD", 2: "SILVER"}
BONUS_BASE_POINTS = 10
BONUS_POINTS = 10

class AttendanceManager:

    def __init__(self):
        self.ids = {}
        self.last_player_id = 0

        # dat[사용자ID][요일]
        self.attendance_count_of_player_per_day = [[0] * 100 for _ in range(100)]
        self.points = [0] * 100
        self.grade = [0] * 100
        self.names = {}
        self.attendance_count_on_wednesday = [0] * 100
        self.attendance_count_on_weekend = [0] * 100

    def manage_attendance(self):
        records = self.read_attendance_weekday_500_file()
        self.count_attendance_day_per_player(records)
        self.calculate_attendance_points_per_player(records)
        self.calculate_bonus_points_per_player()
        self.set_grade_per_player()
        self.print_result_per_player()
        self.print_removed_player()

    def read_attendance_weekday_500_file(self) -> List[List[str]]:
        records: List[List[str]] = []

        attendance_weekday_500_file = Path(__file__).parent / "attendance_weekday_500.txt"
        if not attendance_weekday_500_file.is_file():
            raise FileNotFoundError("파일을 찾을 수 없습니다.")

        with open(attendance_weekday_500_file, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) != 2:
                    raise ValueError("각 레코드는 '이름 요일' 형태로 입력되어야 합니다.")
                records.append(parts)
        return records

    def count_attendance_day_per_player(self, records: List[List[str]]):
        for player_name, attendance_day in records:
            player_id = self.get_player_id(player_name)
            attendance_day_index = self.get_day_index(attendance_day)
            self.attendance_count_of_player_per_day[player_id][attendance_day_index] += 1

    def get_player_id(self, player_name: str) -> int:
        if self.is_new_player(player_name):
            return self.set_new_id(player_name)
        return self.ids[player_name]

    def is_new_player(self, name: str) -> bool:
        return name not in self.ids

    def set_new_id(self, name: str) -> int:
        new_id = self.last_player_id + 1
        self.last_player_id = new_id
        self.ids[name] = new_id
        self.names[self.last_player_id] = name
        return new_id

    def get_day_index(self, attendance_day):
        if attendance_day not in DAY_INDEX.keys():
            raise ValueError("요일에 사용할 수 없는 문자가 유입되었습니다. 사용가능 문자열 : %s", DAY_INDEX.keys())
        return DAY_INDEX[attendance_day]

    def calculate_attendance_points_per_player(self, records: List[List[str]]):
        for player_name, attendance_day in records:
            player_id = self.get_player_id(player_name)
            attendance_day_index = self.get_day_index(attendance_day)
            self.points[player_id] += self.get_attendance_points(attendance_day_index)

    def get_attendance_points(self, attendance_day_index: int) -> int:
        if attendance_day_index == WEDNESDAY:
            return 3
        elif self.is_weekend(attendance_day_index):
            return 2
        return 1

    def is_weekend(self, attendance_day_index: int) -> bool:
        return attendance_day_index == SATURDAY or attendance_day_index == SUNDAY

    def calculate_bonus_points_per_player(self):
        for player_id in sorted(self.ids.values()):
            if self.get_attendance_count_on_wednesday(player_id) >= BONUS_BASE_POINTS:
                self.points[player_id] += BONUS_POINTS
            if self.get_attendance_count_on_weekend(player_id) >= BONUS_BASE_POINTS:
                self.points[player_id] += BONUS_POINTS

    def get_attendance_count_on_wednesday(self, player_id: int) -> int:
        return self.attendance_count_of_player_per_day[player_id][WEDNESDAY]

    def get_attendance_count_on_weekend(self, player_id: int) -> int:
        return self.attendance_count_of_player_per_day[player_id][SATURDAY] + \
            self.attendance_count_of_player_per_day[player_id][SUNDAY]

    def set_grade_per_player(self):
        for player_id in sorted(self.ids.values()):
            self.grade[player_id] = self.evaluate_grade(self.points[player_id])

    def evaluate_grade(self, point: int) -> int:
        if point >= 50:
            return GOLD
        elif point >= 30:
            return SILVER
        return NORMAL

    def print_result_per_player(self):
        for player_id in sorted(self.ids.values()):
            print(f"NAME : {self.names[player_id]}, POINT : {self.points[player_id]}, GRADE : {self.get_grade_name(player_id)}")

    def get_grade_name(self, player_id: int) -> str:
        return GRADE_NAME[self.grade[player_id]]

    def print_removed_player(self):
        print("\nRemoved player")
        print("==============")
        for player_id in sorted(self.ids.values()):
            if self.is_removed_player(player_id):
                print(self.names[player_id])

    def is_removed_player(self, player_id: int) -> bool:
        if self.grade[player_id] in (GOLD, SILVER):
            return False
        if self.get_attendance_count_on_wednesday(player_id) > 0:
            return False
        if self.get_attendance_count_on_weekend(player_id) > 0:
            return False
        return True


if __name__ == "__main__":
    attendance = AttendanceManager()
    attendance.manage_attendance()