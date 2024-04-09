from FlightDesign import Flight
from abc import ABC, abstractmethod

class UserSearch(ABC):
    @abstractmethod
    def search_available_tickets(self):
        pass

class FlightBooking(ABC):
    @abstractmethod
    def book_flight(self, flight):
        pass

class User(UserSearch, FlightBooking):

    def __init__(self,name,flightManager):
        self.name = name
        self.flightManager = flightManager
        self.booking_history = {}

    def search_available_tickets(self):
        print("a. filter flights using source and destination\nb. Filter only business class flights")
        subOption = input("Enter a or b : ").strip().lower()

        class_ = None
        selected_flight = None
        if (subOption == 'a'):

            # filter based on source and destination option 1
            source = input("Enter source : ").strip().lower()
            destination = input("Enter destination : ").strip().lower()
            selected_flight = self.flightManager.search_source_and_destination(source,destination)


        elif (subOption == 'b'):
            selected_flight = self.flightManager.search_class('business')
            class_ = 'business'
        else:
            print('please try again')
            return

        # display filtered flights
        if selected_flight:
            self.book_flight(selected_flight,class_)
        else:
            print("No flights available")



    def book_flight(self,flight,class_):
        if isinstance(flight, Flight):
            ticket = flight.book_flight(self,class_)
            if ticket:
                self.booking_history[ticket.booking_id] = ticket
            else:
                print("Ticket not booked")
