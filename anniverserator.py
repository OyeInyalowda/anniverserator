import argparse
import math

from datetime import date

"""
Anniverserator, never forget how long you've been married again!

Anniverserator is a small python program that will hopefully one day be a small command line utility for persistent tracking of important dates 

Author: Mike Vance
Version: 20251116
"""

# done create an Event class which holds a title and date
# done parse user provided dates
# done calculate time elapsed from date to current time
# TODO save user provided event to file
# TODO read user provided event from file
# done calculate time until next anniversary

class Event:
    """Event consisting of a title and date"""

    def __init__(self, eventName: str = "Default Event", eventDate:date = date(1900, 6, 9)):
        self.eventName = eventName
        self.eventDate = eventDate

    def print_title(self):
        """print event title"""

        print(f"********** {self.eventName} **********")

    def print_ellapsed_days(self):
        """print the days ellapsed between the event and today"""

        # calculate
        ellapsedDays = date.today() - self.eventDate
        
        # print results
        print(f"{ellapsedDays.days} total day(s) since {self.eventDate}")

    def print_ellapsed_years(self):
        """print the years ellapsed between the event and today"""

        # calculate
        ellapsedDays = date.today() - self.eventDate
        ellapsedYears = ellapsedDays.days / 365
        remainder = ellapsedDays.days % 365

        # print results
        if(remainder > 0):
            print(f"{math.floor(ellapsedYears)} year(s) and {remainder} day(s) since {self.eventDate}")
        else:
            print(f"{math.floor(ellapsedYears)} year(s) since {self.eventDate}")

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
#---------- End Event Class ----------#

def main():
    # args and options
    description = "Anniverserator, never forget how long you've been married again!"
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-n", "--Name", 
                        nargs = "*",
                        type  = str,
                        metavar = " ",
                        help  = "New event name. Ex: Our Anniversary")
    parser.add_argument("-d", "--Date", 
                        nargs = 3, 
                        type  = int,
                        metavar = " ",
                        help  = "New event date. Ex: 1901 01 01")
    parser.add_argument("-p", "--Print",
                        action = 'store_true', 
                        help  = "Print event facts")

    #parse args
    args = parser.parse_args()    
    # TODO error check date
    eventDate = date(args.Date[0], args.Date[1], args.Date[2])
    eventName = " ".join(args.Name)
    event = Event(eventName, eventDate)

    if(args.Print):
        event.print_title()
        event.print_ellapsed_years()
        event.print_ellapsed_days()
        event.print_next_occurrence()

if __name__ == "__main__":
    main()


