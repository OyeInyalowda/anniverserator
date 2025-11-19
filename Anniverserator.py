import argparse
import pickle

from datetime import MAXYEAR
from datetime import MINYEAR
from datetime import date
from Event import Event

"""
Anniverserator, never forget how long you've been married again!

Anniverserator is a small python program that will hopefully one day be a small command line utility for persistent tracking of important dates. 

Author: Mike Vance
Version: 0.3
"""

# done create an Event class which holds a title and date
# done parse user provided dates
# done calculate time elapsed from date to current time
# done save user provided event to file
# done read user provided event from file
# TODO create_event() does not handle leap years properly
# TODO create_event does not handle string inputs for months
# done calculate time until next anniversary
# todo functionality to delete events

def save(events) -> bool:
    try:
        with open("events.pickle", "wb") as file:
            pickle.dump(events, file, protocol=pickle.HIGHEST_PROTOCOL)
        file.close()
        print("\nSaving...")
        return True
    except Exception as ex:
        print("Error while pickling object", ex)
        return False

def load(filename: str) -> list:
    result = [] 
    try:
        with open(filename, "rb") as file:
            result = pickle.load(file)
        file.close()
        print("\nLoading...")
    except Exception as ex:
        print("Error while unpickling object", ex)

    return result

def create_events(events: list) -> list :
    """Create new events from user input and return a list of those events"""

    print("**** Create New Anniverserator Event ****")
    print("*   Valid inputs:                       *")                    
    print("*       Title: any                      *")
    print("*       Year: 0 < Year <= 9999          *")
    print("*       Month: 0 < Month <= 12          *")
    print("*       Day: 0 < Day <= # days in month *")
    print("*****************************************")

    correct = False
    anotherEvent = False

    # user input loop
    while(anotherEvent or not correct):
        title = ""
        year = -69
        month = -6
        day = -9

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

        # ask if correct and add to list if so
        print(f"\nEvent Title: {title} | Event Date: {eventDate}")
         
        if input("Is this correct (y/n)? ") == 'y':
            correct = True
            events.append(Event(title, eventDate))

            # ask for another event
            if(input("Would you like to add another event (y/n)? ") == 'y' ):
                anotherEvent = True
            else:
                anotherEvent = False
        else:
            correct = False

    return events

def main():
    # check for existing events
    filename = "events.pickle"
    loadedEvents = load(filename)

    if(not loadedEvents):
        existingEvents = False
        events = []
    else:
        existingEvents = True
        events = loadedEvents

    # args and options
    description = "Anniverserator, never forget how long you've been married again!"
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-n", "--New",
                        action = "store_true", 
                        help  = "Create new events.")
    parser.add_argument("-p", "--Print",
                        action = "store_true", 
                        help  = "Print event facts")

    #parse args
    args = parser.parse_args()    

    if (args.New):
        events = create_events(events)
        existingEvents = True
        save(events)

    if(args.Print and existingEvents):
        for event in events: 
            event.print_title()
            event.print_elapsed_years()
            event.print_elapsed_days()
            event.print_next_occurrence()
    elif(args.Print and not existingEvents):
        print("Uh oh :( No events to print")
        print("Try running Anniverserator again with the -n flag to add new events!")
        
if __name__ == "__main__":
    main()


