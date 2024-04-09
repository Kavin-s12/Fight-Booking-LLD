from datetime import datetime

class TicketBuilder:
    def __init__(self):
        self.booking_id = None
        self.flight = None
        self.user = None
        self.seats = None
        self.seat_class = None
        self.price_per_seat = None
        self.amount = None
        self.meal = None

    def set_booking_id(self, booking_id):
        self.booking_id = booking_id
        return self

    def set_flight(self, flight):
        self.flight = flight
        return self

    def set_user(self, user):
        self.user = user
        return self

    def set_seats(self, seats):
        self.seats = seats
        return self

    def set_seat_class(self, seat_class):
        self.seat_class = seat_class
        return self

    def set_price_per_seat(self, price_per_seat):
        self.price_per_seat = price_per_seat
        return self

    def set_amount(self, amount):
        self.amount = amount
        return self

    def set_meal(self, meal):
        self.meal = meal
        return self

    def build(self):
        return Ticket(self)

class Ticket:
    def __init__(self, builder):
        """
        Initialize a new Ticket object.
        """
        self.booking_id = builder.booking_id
        self.flight = builder.flight
        self.user = builder.user
        self.seats = builder.seats
        self.seat_class = builder.seat_class
        self.date_booked = datetime.now()
        self.price_per_seat = builder.price_per_seat
        self.amount = builder.amount
        self.meal = builder.meal.upper()
        self.status = 'booked'

    def cancel_ticket(self, user):
        """
        Cancel the ticket if the provided user is the same as the user who booked it.
        
        Parameters:
        - user (User): The user attempting to cancel the ticket.
        """
        if self.user != user:
            print('Error: Unauthorized user')
        elif self.status == 'booked':
            self.flight.cancel_ticket(self.booking_id)
            self.status = 'cancelled'
            print('Ticket cancelled successfully')
        else:
            print('Ticket already cancelled')

    def print_summary(self):
        """
        Print a summary of the ticket details.
        """
        print(f'Passenger Name: {self.user.name}')
        print(f'Seats Booked: {self.seats}')
        print(f'Booked Date: {self.date_booked}')
        print(f'Class: {self.seat_class}')
        print(f'Meals Booked: {self.meal}')
        print(f'Status: {self.status}')
        print(f'Paid Amount: {self.amount}')
