from pathlib import Path
from typing import List, Dict

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = (i for i in range(7))
DAY_INDEX = {"monday": MONDAY, "tuesday": TUESDAY, "wednesday": WEDNESDAY, "thursday": THURSDAY, "friday": FRIDAY, "saturday": SATURDAY, "sunday": SUNDAY}

class Attendance:

    def __init__(self):
        self.ids_by_name = {}
        self.player_count = 0

        # dat[사용자ID][요일]
        self.attendance_count_of_player_per_day = [[0] * 100 for _ in range(100)]
        self.points = [0] * 100
        self.grade = [0] * 100
        self.names_by_id = {}
        self.attendance_count_of_wednesday = [0] * 100
        self.attendance_count_of_weekend = [0] * 100

    def get_player_id(self, player_name) -> int:
        if self.is_new_player(player_name):
            self.set_new_id(player_name)

        return self.ids_by_name[player_name]


    def calculate_attendance_points(self, player_id, attendance_day):
        self.update_attendance_count_of_player_per_day(player_id, attendance_day)
        self.points[player_id] += self.get_attendance_points_of(attendance_day)

    def update_attendance_count_of_player_per_day(self, player_id, attendance_day):
        day_index = self.get_day_index_of(attendance_day)
        self.attendance_count_of_player_per_day[player_id][day_index] += 1
        if attendance_day == "wednesday":
            self.attendance_count_of_wednesday[player_id] += 1
        if self.is_weekend(attendance_day):
            self.attendance_count_of_weekend[player_id] += 1

    def get_day_index_of(self, attendance_day):
        if attendance_day not in DAY_INDEX.keys():
            raise ValueError("올바르지 않은 요일명이 입력되었습니다.")
        return DAY_INDEX[attendance_day]

    def get_attendance_points_of(self, attendance_day):
        attendance_point_of_the_day = 1
        if attendance_day == "wednesday":
            attendance_point_of_the_day += 2
        elif self.is_weekend(attendance_day):
            attendance_point_of_the_day += 1
        return attendance_point_of_the_day

    def is_weekend(self, attendance_day):
        return attendance_day == "saturday" or attendance_day == "sunday"

    def is_new_player(self, name):
        return name not in self.ids_by_name

    def set_new_id(self, name):
        self.player_count += 1
        self.ids_by_name[name] = self.player_count
        self.names_by_id[self.player_count] = name

    def read_attendance_weekday_500_file(self) -> List[List[str]]:
        records: List[List[str]] = []

        attendance_weekday_500_file = Path(__file__).parent / "attendance_weekday_500.txt"
        if not attendance_weekday_500_file.is_file():
            print("파일을 찾을 수 없습니다.")
            return records

        with open(attendance_weekday_500_file, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) != 2:
                    print("각 레코드는 '이름 요일' 형태로 입력되어야 합니다.")
                    return []
                records.append(parts)

        return records

    def input_file(self):
        for player_name, attendance_day in self.read_attendance_weekday_500_file():
            self.calculate_attendance_points(self.get_player_id(player_name), attendance_day)

        self.calculate_points()

        self.print_attendance_point_and_grade()

        self.print_removed_player()

    def print_removed_player(self):
        print("\nRemoved player")
        print("==============")
        for player_id in sorted(self.ids_by_name.values()):
            if self.is_removed_player(player_id):
                print(self.names_by_id[player_id])

    def is_removed_player(self, player_id) -> bool:
        if self.grade[player_id] in (1, 2):
            return False
        if self.attendance_count_of_wednesday[player_id] > 0:
            return False
        if self.attendance_count_of_weekend[player_id] > 0:
            return False
        return True

    def print_attendance_point_and_grade(self):
        for player_id in sorted(self.ids_by_name.values()):
            print(f"NAME : {self.names_by_id[player_id]}, POINT : {self.points[player_id]}, GRADE : ", end="")

            if self.grade[player_id] == 1:
                print("GOLD")
            elif self.grade[player_id] == 2:
                print("SILVER")
            else:
                print("NORMAL")

    def calculate_points(self):
        for player_id in sorted(self.ids_by_name.values()):
            if self.attendance_count_of_player_per_day[player_id][2] > 9:
                self.points[player_id] += 10
            if self.attendance_count_of_player_per_day[player_id][5] + self.attendance_count_of_player_per_day[player_id][6] > 9:
                self.points[player_id] += 10

            if self.points[player_id] >= 50:
                self.grade[player_id] = 1
            elif self.points[player_id] >= 30:
                self.grade[player_id] = 2
            else:
                self.grade[player_id] = 0


if __name__ == "__main__":
    attendance = Attendance()
    attendance.input_file()