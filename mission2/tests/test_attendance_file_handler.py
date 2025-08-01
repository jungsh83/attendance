import pytest
from pathlib import Path
from pytest_mock import MockerFixture

from mission2.attendance_file_handler import AttendanceFileHandler

def test_read_attendance_weekday_500_file_성공():
    result = AttendanceFileHandler().read_attendance_weekday_500_file()
    assert len(result) == 500

def test_read_attendance_weekday_500_file_파일없음(mocker: MockerFixture):
    wrong_file_path = Path(__file__).parent / "attendance_weekday_500.txt"
    mocker.patch.object(AttendanceFileHandler, "attendance_weekday_500_file", wrong_file_path)

    with pytest.raises(FileNotFoundError, match="파일을 찾을 수 없습니다."):
        AttendanceFileHandler().read_attendance_weekday_500_file()

def test_read_attendance_weekday_500_file_레코드형태이상함(mocker: MockerFixture):
    wrong_file_path = Path(__file__).parent / "wrong_attendance_weekday.txt"
    mocker.patch.object(AttendanceFileHandler, "attendance_weekday_500_file", wrong_file_path)

    with pytest.raises(ValueError, match="각 레코드는 '이름 요일' 형태로 입력되어야 합니다."):
        AttendanceFileHandler().read_attendance_weekday_500_file()
