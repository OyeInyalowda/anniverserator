import argparse
import pickle
import logging

from datetime import MAXYEAR
from datetime import MINYEAR
from datetime import date
from Event import Event

"""
Anniversarator, never forget how long you've been married again!

Anniversarator is a small python program that will hopefully one day be a small command line utility for persistent tracking of important dates. 

Author: Mike Vance
Version: 0.4
"""

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/debug.log', encoding='utf-8', level=logging.INFO, format="%(asctime)s %(message)s")

def save(events) -> bool:
    try:
        with open("events.pickle", "wb") as file:
            pickle.dump(events, file, protocol=pickle.HIGHEST_PROTOCOL)
        file.close()
        print("\nSaving...")
        return True
    except Exception as ex:
        logger.info(f"Error saving file: {ex}")
        return False

def load(filename: str) -> list:
    result = [] 
    try:
        with open(filename, "rb") as file:
            result = pickle.load(file)
        file.close()
        print("\nLoading...")
    except Exception as ex:
        logger.info(f"Error loading save file: {ex}")

    return result

def create_events(events: list) -> list :

    print("**** Create New Anniversarator Event ****")
    print("*   Valid inputs:                       *")                    
    print("*       Title: any                      *")
    print("*       Year: 0 < Year <= 9999          *")
    print("*       Month: 0 < Month <= 12          *")
    print("*       Day: 0 < Day <= # days in month *")
    print("*****************************************")

    # outer loop - while anotherEvent
    anotherEvent = True
    while(anotherEvent):
        newEvent = Event()

        # accept user input
        title = input("Event title? ")
        yearStr = input("Event year? ")
        monthStr = input("Event month (1 - 12)? ")
        dayStr = input("Event day? ")

        # inner loop - while not valid
        year = 0
        month = 0
        day = 0
        valid = False

        while(not valid):
            if(newEvent.check_year(yearStr) == False):
                logger.info(f"Error - Invalid year: {yearStr}")
                yearStr = input(f"Invalid year. Please enter a value between {MINYEAR} and {MAXYEAR}: ")
            elif(not year):
                year = int(yearStr)

            if(newEvent.check_month(monthStr) == False):
                logger.info(f"Error - Invalid month: {monthStr}")
                monthStr = input(f"Invalid month. Please enter a value between 1 and 12: ")
            elif(not month):
                month = int(monthStr)
            
            if(newEvent.check_day(dayStr) == False):
                logger.info(f"Error - Invalid day: {dayStr}")
                dayStr = input(f"Invalid day. Please enter a value between in range for the given month: ")
            elif(not day):
                day = int(dayStr)

            # check whole date for validity
            if(year and month and day):
                if(newEvent.check_date(year, month, day)):
                    eventDate = date(year, month, day)
                    valid = True
                else:
                    logger.info(f"Error - Invalid day: {dayStr}")
                    dayStr = input(f"Invalid day. Please enter a value between in range for the given month: ")
                    day = 0

        # ask if correct and for another event
        print(f"\nEvent Title: {title} | Event Date: {eventDate}")
        if(input("Is this correct (y/n)? ") == 'y'):
            newEvent = Event(title, eventDate)
            events.append(newEvent)
            
            # ask for another event
            if(input("Would you like to add another event (y/n)? ") == 'y' ):
                anotherEvent = True
            else:
                anotherEvent = False
        else:
            anotherEvent = True

    return events

def main():
    FILENAME = "events.pickle"

    #------------ Handle Args ------------#
    # args and options
    description = "Anniversarator, never forget how long you've been married again!"
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-n", "--New",
                        action = "store_true", 
                        help  = "Create new events.")
    parser.add_argument("-p", "--Print",
                        action = "store_true", 
                        help  = "Print event facts")

    #parse args
    args = parser.parse_args()    


    #------ Anniversarator Behavior ------#
    # check for existing events
    events = load(FILENAME)

    # execute according to arguments
    if(args.New):
        events = create_events(events)
        save(events)

    if(args.Print and events):
        for event in events: 
            event.print_event()
    elif(args.Print and not events):
        print("Uh oh :( No events to print")
        print("Try running Anniversarator again with the -n flag to add new events!")
          
if __name__ == "__main__":
    main()

# done create an Event class which holds a title and date
# done parse user provided dates
# done calculate time elapsed from date to current time
# done save user provided event to file
# done read user provided event from file
# done calculate time until next anniversary
# TODO functionality to delete events
# done add error logging
# done refactor create_events
# done create_event() does not handle leap years properly
# done create_event does not handle string inputs for months
# TODO package project