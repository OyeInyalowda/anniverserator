import argparse
import math
import pickle

from datetime import MAXYEAR
from datetime import MINYEAR
from datetime import date

"""
Anniverserator, never forget how long you've been married again!

Anniverserator is a small python program that will hopefully one day be a small command line utility for persistent tracking of important dates. 

Author: Mike Vance
Version: 0.2
"""

# done create an Event class which holds a title and date
# done parse user provided dates
# done calculate time elapsed from date to current time
# TODO save user provided event to file
# TODO read user provided event from file
# TODO create_event() does not handle leap years properly
# TODO create_event does not handle string inputs for months
# done calculate time until next anniversary

class Event:
    """Event consisting of a title and date"""

    def __init__(self, eventName: str = "Default Event", eventDate:date = date(1900, 6, 9)):
        self.eventName = eventName
        self.eventDate = eventDate

    def print_title(self):
        """print event title"""

        print(f"********** {self.eventName} **********")

    def print_elapsed_days(self):
        """print the days ellapsed between the event and today"""

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
#---------- End Event Class ----------#

#TODO the param for this should be an array of events
def save(event):
    try:
        with open("events.pickle", "wb") as file:
            pickle.dump(event, file, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error while pickling object", ex)

    return #TODO return bool

def create_event() -> Event:
    """Create a new event from user input"""

    print("**** Create New Anniverserator Event ****")
    print("*   Valid inputs:                       *")                    
    print("*       Title: any                      *")
    print("*       Year: 0 < Year <= 9999          *")
    print("*       Month: 0 < Month <= 12          *")
    print("*       Day: 0 < Day <= # days in month *")
    print("*****************************************")

    response = ''
    while(response != 'y'):
        #get title
        title = input("Event title? ")

        # get year
        yearStr = input("Event year? ")
        year = int(yearStr)
        while year < MINYEAR or year > MAXYEAR:
            yearStr = input(f"Invalid year. Please enter a value between {MINYEAR} and {MAXYEAR}: ")
            year = int(yearStr)
        
        # get month
        monthStr = input("Event month (1 - 12)? ")
        month = int(monthStr)
        while month < 1 or month > 12:
            monthStr = input(f"Invalid month. Please enter a value between 1 and 12: ")
            month = int(monthStr)

        # get month
        dayStr = input("Event day? ")
        day = int(dayStr)
        valid = False
        while not valid:
            try:
                eventDate = date(year, month, day)
                valid = True
            except:
                dayStr = input(f"Invalid day. Please enter a value between in range for the given month: ")
                day = int(dayStr)

        # ask if correct
        print(f"\nEvent Title: {title} | Event Date: {eventDate}")
        response = input("Is this correct (y/n)? ")
    
    newEvent = Event(title, eventDate)
    return newEvent

def main():
    # args and options
    description = "Anniverserator, never forget how long you've been married again!"
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-n", "--New",
                        action = 'store_true', 
                        help  = "Create a new event.")
    parser.add_argument("-p", "--Print",
                        action = 'store_true', 
                        help  = "Print event facts")

    #parse args
    args = parser.parse_args()    

    if (args.New):
        event = create_event()
    else:
        event = Event()

    #print
    if(args.Print):
        event.print_title()
        event.print_elapsed_years()
        event.print_elapsed_days()
        event.print_next_occurrence()

if __name__ == "__main__":
    main()


