import uuid
import re
from file_loader import load_flight_details


# book filght ticket
def book_Flight(flight,selected_class):
    flightObj = flight[1]
    booking_id = str(uuid.uuid4())

    check_seats = []
    if selected_class == 'business':
        booked = flightObj.business_booked_seats
        seat_type = flightObj.business_seat_arr[2]
        amount =  flightObj.business_class_price
        row, col = flightObj.business_seat_arr[1]
        if not (row or col):
            print("No business class seats available")
            return
    else:
        booked = flightObj.economy_booked_seats
        seat_type = flightObj.economy_seat_arr[2]
        amount =  flightObj.economy_class_price
        row, col = flightObj.economy_seat_arr[1]
        if not (row or col):
            print("No economy class seats available")
            return

    flightObj.print_available_seats(selected_class = selected_class)
    seats = [seat.strip().upper()  for seat in
                input(f"Choose the seat number in Row(number)_Column(Alphabet) format seperated by comma : ").split(',')]

    if check_seat(seats):    return

    passenger_name = input('Enter your name : ')
    meal = input("Meal required (200 per passenger) (Yes/No) : ").strip().upper()

    while meal not in ('YES', 'NO'):
        meal = input('Please enter either yes or no : ').strip().upper()



    for seat in seats:
        s = seat.split('_')
        book_row = int(s[0])
        book_col = ord(s[1]) - ord('A') + 1

        if book_row > row or book_col > col:
            print(f'{seat} worng seat number!')
            check_seats.append(seat)

        if seat in booked:
            print(f'{seat} is already booked!')
            check_seats.append(seat)

    if len(check_seats) > 0:
        return False


    total_price = 0
    for seat in seats:
        book_col = ord(seat.split('_')[1]) - ord('A')
        booked[seat]  = True if meal == "YES" else False
        total_price += amount + (100 if seat_type[book_col] == 'A' or seat_type[book_col] == 'W' else 0 )

    if meal == 'YES':
        total_price += (200 * len(seats))

    if selected_class == 'business':
        flightObj.business_class_price += 200
        flightObj.business_available_seats -= len(seats)

    else:
        flightObj.economy_class_price += 100
        flightObj.economy_available_seats -= len(seats)


    booking_history[booking_id] = {'seats' : seats, 'flight_name' : flight[0],
                                   'meal' : meal, 'passenger_name' : passenger_name,
                                    'price': total_price, 'class' : selected_class,
                                    'price per seat': amount}
    print(f'\nSuccessfully booked with booking id {booking_id}')
    print_summary(booking_id)
    return True

# cancel ticket
def cancel_ticket(booking_id, cancel_seats):
    if booking_id not in booking_history:
        print("Booking Id not found")
        return False

    details = booking_history[booking_id]
    flightObj = flights[details['flight_name']]

    check_seats = []
    if details['class'] == 'business':
        booked = flightObj.business_booked_seats
        seat_type = flightObj.business_seat_arr[2]
    else:
        booked = flightObj.economy_booked_seats
        seat_type = flightObj.economy_seat_arr[2]

    amount_per_seat =  details['price per seat']

    for seat in cancel_seats:
        if seat not in details['seats']:
            print(f'{seat} is not booked under this booking Id!')
            check_seats.append(seat)

        elif seat not in booked:
            print(f'{seat} is not booked!')
            check_seats.append(seat)

    if len(check_seats) > 0:
        return False

    total_price = details['price']
    refund = 0
    for seat in cancel_seats:
        s = seat.split('_')
        book_col = ord(s[1]) - ord('A')
        booked.pop(seat)
        booking_history[booking_id]['seats'].remove(seat)
        refund += amount_per_seat + (100 if seat_type[book_col] == 'A' or seat_type[book_col] == 'W' else 0 )

    if details["meal"] == "YES":
        refund += 200*len(cancel_seats)

    if selected_class == 'business':
        flightObj.business_class_price += 200
        flightObj.business_available_seats += len(cancel_seats)

    else:
        flightObj.economy_class_price += 100
        flightObj.economy_available_seats += len(cancel_seats)


    booking_history[booking_id]['price'] =  total_price - refund
    refund -= (200 * len(cancel_seats))
    print(f'Cancelled tickets successfully')
    print(f'Refund Amount after deduction Rs.200 per seat: {refund}')
    return True

# print booking summary
def print_summary(booking_id):
    if booking_id not in booking_history:
        print("Booking Id not found")
        return

    details = booking_history[booking_id]
    print(f'        Passenger Name : {details["passenger_name"]}\n\
        Flight Name : {details["flight_name"]}\n\
        Seats Booked : {details["seats"]}\n\
        Class : {details["class"]} \n\
        Meals Booked : {details["meal"]}\n\
        Paid Amount : {details["price"]}')

#close the selected option
def close_option():
    cont = input("\nDo you want to continue (Yes/No) : ").strip().lower()

    while cont.lower() not in ("yes", "no"):
        cont = input("type yes/no only : ")

    if cont == "no":
        print('...closing')
        return True
    return False

#check seat number
def check_seat(seats):
    pattern = r'\d+_([a-zA-Z])'

    for seatNo in seats:
        if not re.match(pattern, seatNo):
           print('Wrong format or No seats selected')
           return True
    return False

#starting of the program
#reads the input
folder_path = "../Flight Details"
flights = load_flight_details(folder_path)

booking_history = {}

while True:
    print("\nPlease select the option.\n1.  List flight details \
        \n2.  Flight Booking\n3.  Cancellation\n4.  Check available seats\
        \n5.  Meal ordered for each flight\n6.  Individual and flight summary\n")
    n = input('Enter the option : ')

    # List all flight details
    if (n == '1'):
        print("Available Flights : ")
        for i,flight in enumerate(flights.items()):
            print(f"{i+1} - {flight[0]}")

        if close_option():
            break

    # Search flight
    elif n == '2':
        print("a. filter flights using source and destination\nb. Filter only business class flights")
        subOption = input("Enter a or b : ").strip().lower()

        filter = []
        if (subOption == 'a'):

            # filter based on source and destination option 1
            source = input("Enter source : ").strip().lower()
            destination = input("Enter destination : ").strip().lower()

            for flight, obj in flights.items():
                if (obj.source == source) and (obj.destination == destination):
                    filter.append((flight, obj))


        elif (subOption == 'b'):

            # filter only business class flights  option 2
            for flight, obj in flights.items():
                if obj.economy_seat_arr[1][0] == 0:
                    filter.append((flight, obj))
        else:
            print('please try again')

        # display filtered flights
        if len(filter) == 0:
            print("No flights available")
        else:
            for i,flight in enumerate(filter):
                print(f"{i+1} - {flight[0]}")

            num = int(input('Select the flight : ')) -1

            if num >= len(filter):
                print('Somthing wrong!')
            else:
                selected_flight = filter[num]
                selected_class = input("Economy or Business class : ").strip().lower()
                while selected_class not in ('business', 'economy'):
                    selected_class = input('Please enter either business or economy : ').strip().lower()
                # book seats
                book_Flight(selected_flight,selected_class)

        if close_option():
            break

    # cancel ticket
    elif n == '3':
        id = input("Please enter your booking id : ").strip()
        cancel_seats = [seat.strip().upper() for seat in input("Enter the seat number to be canceled in Row(number)_Column(Alphabet) format seperated by comma : ").split(',')]

        if check_seat(cancel_seats):
            if close_option():
                break
        else:
            cancel_ticket(id,cancel_seats)

            if close_option():
                break

    # Available seats in all flights
    elif n == '4':
        for flight, obj in flights.items():
            print("\n"+flight)
            obj.print_available_seats()

        if close_option():
            break

    #Meal ordered for each flight
    elif n == '5':
        for flight, obj in flights.items():
            print(flight)
            obj.print_meal_order_list()

        if close_option():
            break

    # Booking summary
    elif n == '6':

        print("a. Individual booking information\nb. summary for all the bookings")
        subOption = input("Enter a or b : ").strip().lower()

        if (subOption == 'a'):
            id = input("Please enter your booking id : ").strip()
            print_summary(id)

        elif (subOption == 'b'):
            if len(booking_history) == 0:
                print('No bookings Yet')
            else:
                for i ,bookId in enumerate(booking_history.keys()):
                    print(f'No {i+1}')
                    print_summary(bookId)
        else:
            print('please try again')

        if close_option():
            break
    else:
        print('Please type the correct option from the list')
