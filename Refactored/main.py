# from LoadFlightDetails import LoadFlightDetails
from FlightDetailsLoader import FlightDetailsLoader
from FlightManager import FlightManager
from User import User

def close_option():
    cont = input("\nDo you want to continue (Yes/No) : ").strip().lower()

    while cont.lower() not in ("yes", "no"):
        cont = input("type yes/no only : ")

    if cont == "no":
        print('...closing')
        return True
    return False

if __name__== '__main__':
    flightManager = FlightManager()
    FlightDetailsLoader(flightManager).load_flight_from_file("../Flight Details")    
    name = input('Enter your name : ')
    testUser = User(name,flightManager)
    print("User name: ",testUser.name)


    # ticket
    while True:
        print("\nPlease select the option.\n1.  List flight details \
            \n2.  Flight Booking\n3.  Cancellation\n4.  Check available seats\
            \n5.  Print ticket summary\n")
        n = input('Enter the option : ')

        # List all flight details
        if (n == '1'):
            FlightManager().list_all_flights()

        # Search flight
        elif n == '2':
            testUser.search_available_tickets()

        # cancel ticket
        elif n == '3':

            if not testUser.booking_history.values():
                print('No bookings')
            else:
                for ticket in testUser.booking_history.values():
                    print(f"Booking Id : {ticket.booking_id} seats : {ticket.seats}")

                id = input('Select the booking Id : ')

                if id not in testUser.booking_history:
                    print('wrong booking Id!')
                else:
                    ticket = testUser.booking_history[id]
                    ticket.cancel_ticket(testUser)

        # Available seats in all flights
        elif n == '4':

            FlightManager().list_all_flights()
            no = input('Enter the Flight No : ')

            if no not in FlightManager().flights:
                print('wrong Flight number')
            else:
                FlightManager().flights[no].print_available_seats()

        # Booking summary
        elif n == '5':

            if not testUser.booking_history.values():
                print('No bookings')
            else:
                for ticket in testUser.booking_history.values():
                    print(f"Booking Id : {ticket.booking_id} seats : {ticket.seats}")

                id = input('Select the booking Id : ')

                if id not in testUser.booking_history:
                    print('wrong booking Id!')
                else:
                    ticket = testUser.booking_history[id]
                    ticket.print_summary()

        else:
            print('Please type the correct option from the list')

        if close_option():
            break
