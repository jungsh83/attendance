from pathlib import Path
from typing import List

class AttendanceFileHandler:
    attendance_weekday_500_file = Path(__file__).parent / "attendance_weekday_500.txt"
    def read_attendance_weekday_500_file(self) -> List[List[str]]:
        records: List[List[str]] = []

        if not self.attendance_weekday_500_file.is_file():
            raise FileNotFoundError("파일을 찾을 수 없습니다.")

        if self._is_inaccurate_file_format():
            raise ValueError("각 레코드는 '이름 요일' 형태로 입력되어야 합니다.")
    
        return self._create_records()

    def _is_inaccurate_file_format(self) -> bool:
        with open(self.attendance_weekday_500_file, encoding='utf-8') as f:
            for line in f.readlines():
                if len(line.strip().split()) != 2:
                    return True
        return False

    def _create_records(self) -> List[List[str]]:
        records: List[List[str]] = []
        with open(self.attendance_weekday_500_file, encoding='utf-8') as f:
            for line in f.readlines():
                parts = line.strip().split()
                records.append(parts)
        return records
