from FlightDesign import Flight
from abc import ABC, abstractmethod, ABCMeta

class FlightManagerInterface(ABC):
    @abstractmethod
    def add_flight(self, flight):
        pass

    @abstractmethod
    def remove_flight(self, flight):
        pass

    @abstractmethod
    def list_all_flights(self):
        pass

    @abstractmethod
    def search_source_and_destination(self, source, destination):
        pass

    @abstractmethod
    def search_class(self, selected_class):
        pass

class Singleton(ABCMeta):
    _instance = {}

    def __call__(cls,*args,**kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton,cls).__call__(*args,**kwargs)

        return cls._instance[cls]

class FlightManager(FlightManagerInterface, metaclass=Singleton ):

    def __init__(self):
        self.flights = {}

    def add_flight(self,flight):
        if isinstance(flight, Flight):
            self.flights[flight.flight_number] = flight

    def remove_flight(self,flight):
        if isinstance(flight, Flight) and flight in self.flights:
            del self.flights[flight.flight_number]

    def list_all_flights(self):
        if not self.flights:
            print("No flights available")
            return

        for flight in self.flights.values():
            print(f'Flight No: {flight.flight_number} From : {flight.source} To : {flight.destination}')
    
    def search_flights(self, criteria):
        matching_flights = [flight for flight in self.flights.values() if criteria(flight)]

        if not matching_flights:
            return None

        for i, flight in enumerate(matching_flights):
            print(f"{i+1} - {flight.flight_number}")

        num = int(input('Select the flight : ')) - 1
        if num >= len(matching_flights):
            print('Invalid selection!')
            return None

        return matching_flights[num]

    def search_source_and_destination(self, source, destination):
        return self.search_flights(lambda flight: flight.source == source and flight.destination == destination)

    def search_class(self, selected_class):
        return self.search_flights(lambda flight: selected_class.lower() in flight.classes and len(flight.classes) == 1)