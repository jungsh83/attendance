#pytest
import sys
import io

import pytest
from pytest_mock import MockerFixture

from mission2.attendance_file_handler import AttendanceFileHandler
from mission2.attendance_manager import AttendanceManager

@pytest.fixture()
def attendance_manager():
    return AttendanceManager()

def test_manage_attendance_성공(attendance_manager):
    result_text = io.StringIO()
    sys.stdout = result_text
    attendance_manager.manage_attendance()

    assert result_text.getvalue() == """NAME : Umar, POINT : 48, GRADE : SILVER
NAME : Daisy, POINT : 45, GRADE : SILVER
NAME : Alice, POINT : 61, GRADE : GOLD
NAME : Xena, POINT : 91, GRADE : GOLD
NAME : Ian, POINT : 23, GRADE : NORMAL
NAME : Hannah, POINT : 127, GRADE : GOLD
NAME : Ethan, POINT : 44, GRADE : SILVER
NAME : Vera, POINT : 22, GRADE : NORMAL
NAME : Rachel, POINT : 54, GRADE : GOLD
NAME : Charlie, POINT : 58, GRADE : GOLD
NAME : Steve, POINT : 38, GRADE : SILVER
NAME : Nina, POINT : 79, GRADE : GOLD
NAME : Bob, POINT : 8, GRADE : NORMAL
NAME : George, POINT : 42, GRADE : SILVER
NAME : Quinn, POINT : 6, GRADE : NORMAL
NAME : Tina, POINT : 24, GRADE : NORMAL
NAME : Will, POINT : 36, GRADE : SILVER
NAME : Oscar, POINT : 13, GRADE : NORMAL
NAME : Zane, POINT : 1, GRADE : NORMAL

Removed player
==============
Bob
Zane
"""

def test_get_player_index_ValueError(attendance_manager):
    with pytest.raises(ValueError, match="등록되지 않은 player입니다."):
        attendance_manager._get_player_index("test_player")

def test_get_day_index(attendance_manager):
    with pytest.raises(ValueError, match="요일에 사용할 수 없는 문자가 유입되었습니다."):
        attendance_manager._get_day_index("test_day")
