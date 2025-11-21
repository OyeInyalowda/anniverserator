from datetime import date
from datetime import MAXYEAR
from datetime import MINYEAR
import math

class Event:
    """Event consisting of a title and date"""

    def __init__(self, eventName: str = "Default Event", eventDate:date = date(1900, 6, 9)):
        self.eventName = eventName
        self.eventDate = eventDate

    def print_event(self):
            self.print_title()
            self.print_elapsed_years()
            self.print_elapsed_days()
            self.print_next_occurrence()
            
    def print_title(self):
        """print event title"""

        print(f"\n********** {self.eventName} **********")

    def print_elapsed_days(self):
        """print the days elapsed between the event and today"""

        # calculate
        elapsedDays = date.today() - self.eventDate
        
        # print results
        print(f"{elapsedDays.days} total day(s) since {self.eventDate}")

    def print_elapsed_years(self):
        """print the years elapsed between the event and today"""

        # calculate
        elapsedDays = date.today() - self.eventDate
        elapsedYears = elapsedDays.days / 365
        remainder = elapsedDays.days % 365

        # print results
        if(remainder > 0):
            print(f"{math.floor(elapsedYears)} year(s) and {remainder} day(s) since {self.eventDate}")
        else:
            print(f"{math.floor(elapsedYears)} year(s) since {self.eventDate}")

    def print_next_occurrence(self):
        """print the date of next occurrence and days until then"""
        futureDate = date(date.today().year, self.eventDate.month, self.eventDate.day)
        daysUntil = futureDate - date.today()

        #if event has already occurred this year then it happens next year
        if(daysUntil.days < 0):
            nextYear = date.today().year + 1
            futureDate = date(nextYear, self.eventDate.month, self.eventDate.day)
            daysUntil = futureDate - date.today()
        elif(daysUntil.days == 0):
            print(f"{self.eventName} is today!!!")
            return

        #print results
        print(f"{self.eventName} occurs next on {futureDate} in {daysUntil.days} day(s)")


    def check_year(self, yearStr: str) -> bool:
        """checks if provided year is an integer in valid range"""
        try:
            year = int(yearStr)
        except:
            return False
        
        if(year < MINYEAR or year > MAXYEAR):
            return False
        else:
            return True

    def check_month(self, monthStr: str) -> bool:
        """checks if provided month is an integer in valid range"""

        try:
            month = int(monthStr)
        except:
            return False
        
        if(month < 1 or month > 12):
            return False
        else:
            return True

    def check_day(self, dayStr: str) -> bool:
        """only checks if provided day is an integer"""
        try:
            day = int(dayStr)
        except:
            return False
        
        if(day <= 0 or day > 31):
            return False
        else:
            return True

    def check_date(self, year: int, month: int, day: int):
        try:
            eventDate = date(year, month, day)
            return True
        except:
            return False  
#---------- End Event Class ----------#
