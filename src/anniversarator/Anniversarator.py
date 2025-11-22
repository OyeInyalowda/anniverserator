import argparse
import pickle
import logging

from pathlib import Path
from datetime import date
from datetime import MAXYEAR
from datetime import MINYEAR
from anniversarator.Event import Event

"""
Anniversarator, never forget how long you've been married again!

Anniversarator is a small python command line utility for persistent tracking of important dates. 

Author: Mike Vance
"""

logDir = Path.home() / ".anniversarator" / "logs"
logDir.mkdir(parents=True, exist_ok=True)
logFile = logDir / "debug.log"
saveDir = Path.home() / ".anniversarator" / "saves"
saveDir.mkdir(parents=True, exist_ok=True)
saveFile = saveDir / "events.pickle"

logger = logging.getLogger(__name__)
logging.basicConfig(filename=str(logFile), encoding='utf-8', level=logging.INFO, format="%(asctime)s %(message)s")

def __save(events: dict[str, Event], filename: str) -> bool:
    """Save the given event using the pickle module."""

    try:
        with open(filename, "wb") as file:
            pickle.dump(events, file, protocol=pickle.HIGHEST_PROTOCOL)
        file.close()
        print("\nSaving...")
        return True
    except Exception as ex:
        logger.info(f"Error saving file: {ex}")
        return False

def __load(filename: str) -> dict[str, Event]:
    """Load event(s) from the given pickle filename"""

    result = {} 
    try:
        with open(filename, "rb") as file:
            result = pickle.load(file)
        file.close()
        print("\nLoading...")
    except Exception as ex:
        logger.info(f"Error loading save file: {ex}")

    return result

def create_events(events: dict[str, Event]) -> dict[str, Event]:
    """Create a list of events from user input."""

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
            events.update({title: newEvent})
            
            # ask for another event
            if(input("Would you like to add another event (y/n)? ") == 'y' ):
                anotherEvent = True
            else:
                anotherEvent = False
                break
        else:
            anotherEvent = True

    return events

def __delete_events(events: dict[str, Event]) -> dict[str, Event]:
    """Delete events according to user input."""

    anotherEvent = True
    titles = events.keys()

    while(anotherEvent):

        # check if there are any events
        if(events == {}):
            print("Nothing to delete!")
            break
        
        # print events available to delete
        print("Events: ")
        for title in titles:
            print(f"  {title}")

        # attempt to remove user requested event
        target = input("Enter the title of the event you would like to delete. ")
        if(titles.__contains__(target)):
            events.pop(target)
            print(f"Removing {target}")
        else:
            print("Hmm, that event doesn't seem to be here.")

        # prompt user to remove another event
        if((input("Would you like to delete another event (y/n)? ")) == "y"):
            anotherEvent = True
        else:
            anotherEvent = False
            break
    
    return events


def main():
    FILENAME = "saves/events.pickle"


    #------------ Handle Args ------------#
    # args and options
    description = "Anniversarator, never forget how long you've been married again!"
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-n", "--new",
                        action = "store_true", 
                        help  = "Create new events.")
    parser.add_argument("-p", "--print",
                        action = "store_true", 
                        help  = "Print all events")
    parser.add_argument("-d", "--delete",
                        action = "store_true", 
                        help  = "Delete events") # TODO rm

    #parse args
    args = parser.parse_args()    

    #------ Anniversarator Behavior ------#
    # check for existing events
    events = __load(str(saveFile))

    if(args.delete):
        __delete_events(events)
        __save(events, str(saveFile))

    # execute according to arguments
    if(args.new):
        events = create_events(events)
        __save(events, str(saveFile))

    if(args.print and events):
        for event in events: 
            events[event].print_event()
    elif(args.print and not events):
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
# done functionality to delete events
# done add error logging
# done refactor create_events
# done create_event() does not handle leap years properly
# done create_event does not handle string inputs for months
# done package project
# TODO add next upcoming event function
# TODO add delete all function