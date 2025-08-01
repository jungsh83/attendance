from typing import List
from mission2.grade import Grade, NormalGrade, GradeFactory
from mission2.attendance_file_handler import AttendanceFileHandler
from mission2.player import Player
from mission2.config import config

class AttendanceManager:
    players: List[Player]
    def __init__(self):
        self.players = []
        self.file_handler: AttendanceFileHandler = AttendanceFileHandler()

    def manage_attendance(self):
        records = self.file_handler.read_attendance_weekday_500_file()
        self.create_players(records)
        self.count_attendance_day_per_player(records)
        self.calculate_attendance_points_per_player(records)
        self.calculate_bonus_points_per_player()
        self.set_grade_per_player()
        self.print_result_per_player()
        self.print_removed_player()

    def create_players(self, records: List[List[str]]):
        for player_name, _ in records:
            if self._is_new_player(player_name):
                self._add_player(player_name)

    def _add_player(self, player_name: str):
        new_player = Player(id=len(self.players), name=player_name)
        self.players.append(new_player)

    def _is_new_player(self, player_name: str) -> bool:
        for player in self.players:
            if player.name == player_name:
                return False
        return True

    def _get_player_index(self, player_name: str) -> int:
        for index, player in enumerate(self.players):
            if player.name == player_name:
                return index
        raise ValueError("등록되지 않은 player입니다.")

    def count_attendance_day_per_player(self, records: List[List[str]]):
        for player_name, attendance_day in records:
            player_index = self._get_player_index(player_name)
            attendance_day_index = self._get_day_index(attendance_day)
            self.players[player_index].attendance_count[attendance_day_index] += 1

    def _get_day_index(self, attendance_day):
        if attendance_day not in config.DAY_INDEX.keys():
            raise ValueError("요일에 사용할 수 없는 문자가 유입되었습니다.")
        return config.DAY_INDEX[attendance_day]

    def calculate_attendance_points_per_player(self, records: List[List[str]]):
        for player_name, attendance_day in records:
            player_index = self._get_player_index(player_name)
            attendance_day_index = self._get_day_index(attendance_day)
            self.players[player_index].points += self._get_attendance_points(attendance_day_index)

    def _get_attendance_points(self, attendance_day_index: int) -> int:
        if attendance_day_index == config.WEDNESDAY:
            return 3
        elif self._is_weekend(attendance_day_index):
            return 2
        return 1

    def _is_weekend(self, attendance_day_index: int) -> bool:
        return attendance_day_index == config.SATURDAY or attendance_day_index == config.SUNDAY

    def calculate_bonus_points_per_player(self):
        for player in self.players:
            if player.attendance_count_on_wednesday >= config.BONUS_BASE_POINTS:
                player.points += config.BONUS_POINTS
            if player.attendance_count_on_weekend >= config.BONUS_BASE_POINTS:
                player.points += config.BONUS_POINTS

    def set_grade_per_player(self):
        for player in self.players:
            player.grade = GradeFactory.get_grade(player.points)

    def print_result_per_player(self):
        for player in self.players:
            print(f"NAME : {player.name}, POINT : {player.points}, GRADE : {player.grade.name}")

    def print_removed_player(self):
        print("\nRemoved player")
        print("==============")
        for player in self.players:
            if self._is_removed_player(player):
                print(player.name)

    def _is_removed_player(self, player: Player) -> bool:
        if not isinstance(player.grade, NormalGrade):
            return False
        if player.attendance_count_on_wednesday > 0:
            return False
        if player.attendance_count_on_weekend > 0:
            return False
        return True
