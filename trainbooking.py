import streamlit as st

class train:
    def __init__(self, train_num, schedule, time, total_seats):
        self.train_num = train_num
        self.schedule = schedule
        self.time = time
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.bookings = {}

class railway_system:
    def __init__(self):
        self.trains = {
            "T101": train("T101", "mon, wed, fri", "10:00 AM", 50),
            "T102": train("T102", "tue, thu, sat", "2:00 PM", 40)
        }
        self.all_bookings = {}

    def check_availability(self, train_num, date):
        if train_num not in self.trains:
            return False, f"train {train_num} doesn’t exist"
        train = self.trains[train_num]
        if date.lower() not in train.schedule:
            return False, f"train {train_num} doesn’t run on {date}"
        return True, f"available seats on {train_num} for {date}: {train.available_seats}"

    def book_ticket(self, passenger, train_num, date, seats):
        available, msg = self.check_availability(train_num, date)
        if not available:
            return False, msg
        train = self.trains[train_num]
        if seats > train.available_seats:
            return False, f"only {train.available_seats} seats left, can’t book {seats}"
        train.available_seats -= seats
        train.bookings[passenger] = [date, seats]
        if passenger not in self.all_bookings:
            self.all_bookings[passenger] = {}
        self.all_bookings[passenger][train_num] = [date, seats]
        return True, f"booked {seats} seats for {passenger} on {train_num} for {date}"

    def cancel_ticket(self, passenger, train_num):
        if train_num not in self.trains or passenger not in self.trains[train_num].bookings:
            return False, "no booking found"
        train = self.trains[train_num]
        seats = train.bookings[passenger][1]
        train.available_seats += seats
        del train.bookings[passenger]
        del self.all_bookings[passenger][train_num]
        if not self.all_bookings[passenger]:
            del self.all_bookings[passenger]
        return True, f"cancelled {passenger}’s booking on {train_num}"

    def modify_booking(self, passenger, train_num, new_date, new_seats):
        if train_num not in self.trains or passenger not in self.trains[train_num].bookings:
            return False, "no booking found to modify"
        success, msg = self.cancel_ticket(passenger, train_num)
        if success:
            return self.book_ticket(passenger, train_num, new_date, new_seats)
        return False, msg

    def view_bookings(self, passenger):
        if passenger in self.all_bookings:
            return True, f"{passenger}’s bookings: {self.all_bookings[passenger]}"
        return False, "no bookings found"

    def admin_view(self):
        if not self.all_bookings:
            return False, "no bookings yet"
        bookings_str = "ALL BOOKINGS:\n"
        for passenger, details in self.all_bookings.items():
            bookings_str += f"{passenger}: {details}\n"
        return True, bookings_str

def main(): #test push
    st.title("Railway booking system")
    system = railway_system()
    if "system" not in st.session_state:
        st.session_state.system = system

    option = st.sidebar.selectbox("MENU", ["book ticket", "cancel ticket", "modify ticket", "view bookings", "admin view"])

    if option == "book ticket":
        passenger = st.text_input("Your name")
        train_num = st.selectbox("pick a train", ["T101", "T102"])
        date = st.text_input("date (like mon)")
        seats = st.number_input("how many seats", min_value=1, step=1)
        if st.button("book it"):
            success, msg = st.session_state.system.book_ticket(passenger, train_num, date, seats)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    elif option == "cancel ticket":
        passenger = st.text_input("Your name")
        train_num = st.selectbox("pick a train", ["T101", "T102"])
        if st.button("cancel it"):
            success, msg = st.session_state.system.cancel_ticket(passenger, train_num)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    elif option == "modify ticket":
        passenger = st.text_input("Your name")
        train_num = st.selectbox("pick a train", ["T101", "T102"])
        new_date = st.text_input("new date")
        new_seats = st.number_input("new seat count", min_value=1, step=1)
        if st.button("modify it"):
            success, msg = st.session_state.system.modify_booking(passenger, train_num, new_date, new_seats)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    elif option == "view bookings":
        passenger = st.text_input("Your name")
        if st.button("check it"):
            success, msg = st.session_state.system.view_bookings(passenger)
            if success:
                st.write(msg)
            else:
                st.error(msg)

    elif option == "admin view":
        if st.button("show all"):
            success, msg = st.session_state.system.admin_view()
            if success:
                st.write(msg)
            else:
                st.error(msg)

if __name__ == "__main__":
    main()