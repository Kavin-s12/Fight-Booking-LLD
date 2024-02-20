class Flight:
    def __init__(self, flight_number, source, destination,business_seat_arr,economy_seat_arr):
        self.flight_number = flight_number
        self.source = source
        self.destination = destination
        self.business_seat_arr = business_seat_arr
        self.economy_seat_arr = economy_seat_arr
        self.business_booked_seats = {}
        self.economy_booked_seats = {}
        self.business_class_price = 2000
        self.economy_class_price = 1000
        self.business_available_seats = business_seat_arr[1][0] * business_seat_arr[1][1]
        self.economy_available_seats = economy_seat_arr[1][0] * economy_seat_arr[1][1]
        

    def print_available_seats(self,selected_class = None):
        
        if (selected_class == None or selected_class == 'business'):
            print(f'\nAvailable Business Class tickets: {self.business_available_seats}')
            if self.business_available_seats :
                row = self.business_seat_arr[1][0]
                col = self.business_seat_arr[1][1]
                for i in range(1,row+1):
                    for j in range(col):
                        seatNo = str(i)+'_'+chr(65+j)
                        if seatNo not in self.business_booked_seats:
                            print(seatNo,end=', ')
                        else:
                            print(' x ',end=', ')
                    print()
        
        if (selected_class == None or selected_class == 'economy'):
            print(f'\nAvailable Economy Class tickets: {self.economy_available_seats}')
            if self.economy_available_seats:                
                row = self.economy_seat_arr[1][0]
                col = self.economy_seat_arr[1][1]
                for i in range(1,row+1):
                    for j in range(col):
                        seatNo = str(i)+'_'+chr(65+j)
                        if seatNo not in self.economy_booked_seats:
                            print(seatNo,end=', ')
                        else:
                            print(' x ',end=', ')
                    print()
                
    def print_meal_order_list(self):
        business = [seat for seat,meal in self.business_booked_seats.items() if meal]
        economy = [seat for seat,meal in self.economy_booked_seats.items() if meal]
        print(f"Business Class : { ', '.join(business) if len(business) > 0 else 'No meals ordered'}")
        print(f"Economy Class : {', '.join(economy) if len(economy) > 0 else 'No meals ordered'} \n")