import os
from FlightDesign import Flight, SeatClass

class FlightDetailsLoader:
    def __init__(self, flight_manager):
        self.flight_manager = flight_manager
        self.special_seat_price = 200
        self.ticket_price = 1000

    def load_flight_from_file(self, folder_path):
        try:
            for filename in os.listdir(folder_path):
                if filename.endswith(".txt"):
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, "r") as file:
                        flight = self.parse_flight_from_file(file)
                        if flight:
                            self.flight_manager.add_flight(flight)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")

    def parse_flight_from_file(self, file):
        try:
            name = os.path.basename(file.name).split('.txt')[0]
            details = name.split('-')

            flight = Flight(details[1], details[2].lower(), details[3].lower())

            for line in file:
                class_info, seats_info = line.strip().split(" : ")
                part_list = [int(num.strip('{}')) for num in seats_info.split(', ')[0:-1]]
                structure = self.calculate_structure(part_list)

                row = int(seats_info.split(', ')[-1])
                col = sum(part_list)

                if  row >0 and col>0:
                    flight.add_seat_class(class_info.lower(), structure, self.ticket_price, row, col, self.special_seat_price)

            return flight
        
        except Exception as e:
            print(f"Error parsing file: {e}")
            return None

    def calculate_structure(self, part_list):
        if sum(part_list) == 1:
            return 'W'
        else:
            structure = ''
            for i in part_list:
                if i == 0:
                    continue
                if i > 1:
                    st = 'A' + 'M' * (i - 2) + 'A'
                else:
                    st = 'A'
                structure += st
            return 'W' + structure[1:-1] + 'W'
