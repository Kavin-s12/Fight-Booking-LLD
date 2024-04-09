import re
import uuid
from Ticket import Ticket, TicketBuilder

class Flight:

    def __init__(self, flight_number, source, destination):
        self.flight_number = flight_number
        self.source = source
        self.destination = destination
        self.classes =  {}

    def book_flight(self,user,selected_class):
        if not selected_class:
            self.print_available_seats()
            selected_class = input('Please enter seat class : ').strip().lower()
        if selected_class not in self.classes:
            print(f'No {selected_class} class seats available')
            return None

        return self.classes[selected_class].book_ticket(user)

    def print_available_seats(self):
        for seat_class in self.classes.values():
            seat_class.print_available_seats()

    def add_seat_class(self, name, seat_pattern, price, rows, columns, special_seat_price):
        self.classes[name.lower()] = SeatClass(name, seat_pattern, price, rows, columns, special_seat_price)

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
        self.meal_price = 200
        self.cancel_charges = 200

    def print_available_seats(self):

        print(f'\nAvailable {self.name} Class tickets: ')

        for i in range(1,self.no_of_rows+1):
            for j in range(self.no_of_columns):
                seat_no = str(i)+'_'+chr(65+j)
                print(seat_no if seat_no not in self.booked_seats else ' x ', end=', ')
            print()

    def get_input(self):
        seats = [seat.strip().upper()  for seat in
                    input(f"Choose the seat number in Row(number)_Column(Alphabet) format seperated by comma : ").split(',')]

        if not all(re.match(r'\d+_[a-zA-Z]', seat) for seat in seats):
            print('Wrong format or no seats selected')
            return [], ''

        meal = input(f"Meal required ({self.meal_price} per passenger) (Yes/No) : ").strip().upper()

        while meal not in ('YES', 'NO'):
            meal = input('Please enter either yes or no : ').strip().upper()

        return seats,meal


    def book_ticket(self,user):
        self.print_available_seats()

        seats,meal = self.get_input()

        if self.is_invalid_seats(seats) or not seats:
            return False

        booking_id = str(uuid.uuid4())
        total_price = sum(self.calculate_seat_price(seat,meal) for seat in seats)
        
        ticket_builder = TicketBuilder() \
            .set_booking_id(booking_id) \
            .set_flight(self) \
            .set_user(user) \
            .set_seats(seats) \
            .set_seat_class(self.name) \
            .set_price_per_seat(self.price) \
            .set_amount(total_price) \
            .set_meal(meal)
        ticket = ticket_builder.build()
        self.update_booked_seats(seats, meal)
        self.booking_history[booking_id] = ticket

        print(f'\nSuccessfully booked with booking id {booking_id}')
        ticket.print_summary()

        return ticket

    def calculate_seat_price(self, seat, meal):
        column_index = ord(seat.split('_')[1]) - ord('A')
        return self.price + (self.special_seat_price if self.seat_pattern[column_index] in ('A', 'W') else 0) + (200 if meal == 'YES' else 0)
    

    def is_invalid_seats(self, seats):
        invalid_seats = [seat for seat in seats if self.is_invalid_seat(seat)]
        if invalid_seats:
            print('Invalid seat numbers:', ', '.join(invalid_seats))
            return True
        return False

    def is_invalid_seat(self, seat):
        row, column = seat.split('_')
        if int(row) > self.no_of_rows or not 'A' <= column <= chr(65 + self.no_of_columns - 1):
            print(f'{seat} - Invalid seat')
            return True
        if seat in self.booked_seats:
            print(f'{seat} - Seat already booked')
            return True
        return False

    def update_booked_seats(self, seats, meal):
        for seat in seats:
            self.booked_seats[seat] = meal == 'YES'


    def cancel_ticket(self,booking_id):
        if booking_id not in self.booking_history:
            print("Booking Id not found")
            return False

        ticket = self.booking_history[booking_id]

        for seat in ticket.seats:
            if seat in self.booked_seats:
                del self.booked_seats[seat]

        refund = ticket.amount - (self.cancel_charges * len(ticket.seats))
        print(f'Refund Amount after deduction Rs.{self.cancel_charges} per seat: {refund}')
        return True
