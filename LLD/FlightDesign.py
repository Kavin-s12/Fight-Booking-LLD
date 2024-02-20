import re
import uuid
from Ticket import Ticket

class Flight:

    def __init__(self, flight_number, source, destination, classes = None):
        self.flight_number = flight_number
        self.source = source
        self.destination = destination
        self.classes = classes if classes is not None else {}

    def book_flight(self,user,selected_class):
        if not selected_class:
            for seat in self.classes.keys():
                print(f"{seat}")

            selected_class = input('Please enter seat class : ').strip().lower()
        if selected_class not in self.classes:
            print(f'No {selected_class} class seats available')
            return None

        return self.classes[selected_class].book_ticket(user)

    def print_available_seats(self):
        for seat_class in self.classes.values():
            seat_class.print_available_seats()



class SeatClass:

    def __init__(self,name,seat_pattern,price,rows,columns,special_seat_price):
        self.name = name
        self.seat_pattern = seat_pattern
        self.price = price
        self.no_of_rows = rows
        self.no_of_columns = columns
        self.booked_seats = {}
        self.booking_history = {}
        self.special_seat_price = special_seat_price

    def print_available_seats(self):

        print(f'\nAvailable {self.name} Class tickets: ')

        for i in range(1,self.no_of_rows+1):
            for j in range(self.no_of_columns):
                seatNo = str(i)+'_'+chr(65+j)
                if seatNo not in self.booked_seats:
                    print(seatNo,end=', ')
                else:
                    print(' x ',end=', ')
            print()

    #check seat number
    def check_seat(self,seats):
        pattern = r'\d+_([a-zA-Z])'

        for seatNo in seats:
            if not re.match(pattern, seatNo):
                return True
        return False

    def get_input(self):
        seats = [seat.strip().upper()  for seat in
                    input(f"Choose the seat number in Row(number)_Column(Alphabet) format seperated by comma : ").split(',')]

        if self.check_seat(seats):
            print('Wrong format or No seats selected')
            return [],''

        meal = input("Meal required (200 per passenger) (Yes/No) : ").strip().upper()

        while meal not in ('YES', 'NO'):
            meal = input('Please enter either yes or no : ').strip().upper()

        return seats,meal

    def check_seats(self,seats):
        check_seats = []
        for seat in seats:
            s = seat.split('_')
            book_row = int(s[0])
            book_col = ord(s[1]) - ord('A') + 1

            if book_row > self.no_of_rows or book_col > self.no_of_columns:
                print(f'{seat} worng seat number!')
                check_seats.append(seat)

            if seat in self.booked_seats:
                print(f'{seat} is already booked!')
                check_seats.append(seat)

        if len(check_seats) > 0:
            return True


    def book_ticket(self,user):
        self.print_available_seats()

        seats,meal = self.get_input()

        if self.check_seats(seats) or not seats:
            return False

        booking_id = str(uuid.uuid4())
        total_price = 0
        for seat in seats:
            book_col = ord(seat.split('_')[1]) - ord('A')
            self.booked_seats[seat]  = True if meal == "YES" else False
            total_price += self.price + (self.special_seat_price if self.seat_pattern[book_col] == 'A' or self.seat_pattern[book_col] == 'W' else 0 )

        if meal == 'YES':
            total_price += (200 * len(seats))

        ticket = Ticket(booking_id,self,user,seats,self.name,self.price,meal,total_price)
        self.booking_history[booking_id] = ticket
        print(f'\nSuccessfully booked with booking id {booking_id}')

        ticket.print_summary()

        return ticket

    def cancel_ticket(self,booking_id):
        if booking_id not in self.booking_history:
            print("Booking Id not found")
            return False


        ticket = self.booking_history[booking_id]
        refund = 0

        for seat in ticket.seats:
            if seat in self.booked_seats:
                del self.booked_seats[seat]

        refund = ticket.amount - (200 * len(ticket.seats))
        print(f'Refund Amount after deduction Rs.200 per seat: {refund}')
        return True
