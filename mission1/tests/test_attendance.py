#pytest
import sys
import io

import pytest


from mission1.attendance_manager import AttendanceManager

def test_attendance():
    result_text = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = result_text

    attendance = AttendanceManager()
    attendance.manage_attendance()

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
    sys.stdout = original_stdout
