from pathlib import Path

class Attendance:

    def __init__(self):
        self.id1 = {}
        self.id_cnt = 0

        # dat[사용자ID][요일]
        self.dat = [[0] * 100 for _ in range(100)]
        self.points = [0] * 100
        self.grade = [0] * 100
        self.names = [''] * 100
        self.wed = [0] * 100
        self.weekend = [0] * 100

    def input2(self, w, wk):

        if w not in self.id1:
            self.id_cnt += 1
            self.id1[w] = self.id_cnt
            self.names[self.id_cnt] = w

        id2 = self.id1[w]

        add_point = 0
        index = 0

        if wk == "monday":
            index = 0
            add_point += 1
        elif wk == "tuesday":
            index = 1
            add_point += 1
        elif wk == "wednesday":
            index = 2
            add_point += 3
            self.wed[id2] += 1
        elif wk == "thursday":
            index = 3
            add_point += 1
        elif wk == "friday":
            index = 4
            add_point += 1
        elif wk == "saturday":
            index = 5
            add_point += 2
            self.weekend[id2] += 1
        elif wk == "sunday":
            index = 6
            add_point += 2
            self.weekend[id2] += 1

        self.dat[id2][index] += 1
        self.points[id2] += add_point


    def read_attendance_weekday_500_file(self):
        try:
            with open(Path(__file__).parent / "attendance_weekday_500.txt", encoding='utf-8') as f:
                for _ in range(500):
                    line = f.readline()
                    if not line:
                        break
                    parts = line.strip().split()
                    if len(parts) == 2:
                        self.input2(parts[0], parts[1])
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")

    def input_file(self):
        self.read_attendance_weekday_500_file()

        self.calculate_points()

        self.print_attendance_point_and_grade()

        self.print_removed_player()

    def print_removed_player(self):
        print("\nRemoved player")
        print("==============")
        for i in range(1, self.id_cnt + 1):
            if self.is_removed_player(i):
                print(self.names[i])

    def is_removed_player(self, i):
        return self.grade[i] not in (1, 2) and self.wed[i] == 0 and self.weekend[i] == 0

    def print_attendance_point_and_grade(self):
        for i in range(1, self.id_cnt + 1):
            print(f"NAME : {self.names[i]}, POINT : {self.points[i]}, GRADE : ", end="")

            if self.grade[i] == 1:
                print("GOLD")
            elif self.grade[i] == 2:
                print("SILVER")
            else:
                print("NORMAL")

    def calculate_points(self):
        for i in range(1, self.id_cnt + 1):
            if self.dat[i][3] > 9:
                self.points[i] += 10
            if self.dat[i][5] + self.dat[i][6] > 9:
                self.points[i] += 10

            if self.points[i] >= 50:
                self.grade[i] = 1
            elif self.points[i] >= 30:
                self.grade[i] = 2
            else:
                self.grade[i] = 0


if __name__ == "__main__":
    attendance = Attendance()
    attendance.input_file()