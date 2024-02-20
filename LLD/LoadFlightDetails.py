import os
from FlightManager import FlightManager
from FlightDesign import Flight, SeatClass

class LoadFlightDetails:
    def __init__(self):
        pass

    def load_flight(self,folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                name = str(filename).split('.txt')[0]
                details = name.split('-')

                flight = Flight(details[1],details[2].lower(),details[3].lower())
                # Open and read the contents of the file
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r") as file:
                    for line in file:
                        # Split the line into class and seat arrangement
                        class_info, seats_info = line.strip().split(" : ")
                        parts = seats_info.split(', ')

                        # Split the set part into individual numbers
                        part_list = [int(num.strip('{}')) for num in parts[0:-1]]
                        col = sum(part_list)

                        # Extract the last number (as an integer)
                        row = int(parts[-1])

                        #structure
                        structure = ''
                        if col == 1:
                            structure = 'W'
                        else:
                            structure = ''
                            for i in part_list:
                                if i == 0:
                                    continue
                                if i>1:
                                    st = 'A'+'M'*(i-2)+'A'
                                else:
                                    st = 'A'
                                structure += st
                            structure = 'W'+structure[1:-1]+'W'
                        
                        seat = SeatClass(class_info.lower(),structure,1000,row,col,200)
                        flight.classes[class_info.lower()] = seat

                FlightManager().add_flight(flight)
