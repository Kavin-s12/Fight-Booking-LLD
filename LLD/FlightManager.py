from FlightDesign import Flight

class Singleton(type):
    _instance = {}

    def __call__(cls,*args,**kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton,cls).__call__(*args,**kwargs)

        return cls._instance[cls]

class FlightManager(metaclass =Singleton ):

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
            print(f'Name: {flight.flight_number} From : {flight.source} To : {flight.destination}')

    def search_source_and_destination(self,source,destination):
        matching_flights = [flight for flight in self.flights.values() if
                        flight.source == source and flight.destination == destination]

        for i,flight in enumerate(matching_flights):
            print(f"{i+1} - {flight.flight_number}")

        if not matching_flights:
            return None

        num = int(input('Select the flight : ')) -1

        if num >= len(matching_flights):
            print('wrong number!')
        else:
            return matching_flights[num]

        return None

    def search_class(self,selected_class):
        if not selected_class:
            return None

        matching_flights = [flight for flight in self.flights.values() if
                        selected_class.lower() in flight.classes]

        for i,flight in enumerate(matching_flights):
            print(f"{i+1} - {flight.flight_number}")

        num = int(input('Select the flight : ')) -1
        if num >= len(matching_flights):
            print('wrong number!')
        else:
            return matching_flights[num]

        return None
