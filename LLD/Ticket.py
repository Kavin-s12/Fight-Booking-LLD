from datetime import datetime

class Ticket:

    def __init__(self,booking_id,Flight,User,seats,seat_class,price_per_seat,meal,amount):
        self.booking_id = booking_id
        self.Flight = Flight
        self.User = User
        self.seats = seats
        self.seat_class = seat_class
        self.date_booked = datetime.now()
        self.price_per_seat = price_per_seat
        self.amount = amount
        self.meal = meal.upper()
        self.status = 'booked'

    def cancel_ticket(self,user):
        if self.User != user:
            print('Wrong user')
        elif self.status == 'booked' :
            self.Flight.cancel_ticket(self.booking_id)
            self.status = 'cancelled'
            print('Ticket cancelled')
        else:
            print('Ticket already cancelled')

    def print_summary(self):
        print(f'\tPassenger Name : {self.User.name}\n\
            Seats Booked : {self.seats}\n\
            Booked date : {self.date_booked} \n\
            Class : {self.seat_class} \n\
            Meals Booked : {self.meal}\n\
            Status : {self.status}\n\
            Paid Amount : {self.amount}')
