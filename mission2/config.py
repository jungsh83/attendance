class Config:
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = (i for i in range(7))
    DAY_INDEX = {"monday": MONDAY, "tuesday": TUESDAY, "wednesday": WEDNESDAY, "thursday": THURSDAY, "friday": FRIDAY, "saturday": SATURDAY, "sunday": SUNDAY}
    BONUS_BASE_POINTS = 10
    BONUS_POINTS = 10

config = Config()