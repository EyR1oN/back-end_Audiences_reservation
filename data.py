from models import *
from sqlalchemy import create_engine

user1 = User(username="Col1ns", firstName="Taras", lastName="Vovk", email="customemail@gmail.com", password="asdf",
             phoneNumber="0935215742")

audience1 = Audience(number=12)

status1 = Status(statusName="Available")

reservation1 = Reservation(idAudience=1, idUser=1, idStatus=1,
                           amountOfHours=4, dateTimeOfReservation="28.10.2021", dateTimeOfEndReservation="30.11.2021")

user2 = User(username="Starvars", firstName="Danylo", lastName="Sarvas", email="dsadf@gmail.com", password="pass",
             phoneNumber="102")


status2 = Status(statusName="Unavailable")

reservation2 = Reservation(idAudience=1, idUser=2, idStatus=2,
                           amountOfHours=4, dateTimeOfReservation="28.10.2021", dateTimeOfEndReservation="30.11.2021")

user3 = User(username="hjkda", firstName="Max", lastName="Los", email="destr@gmail.com", password="1234",
             phoneNumber="103")
audience2 = Audience(number=11)
reservation3 = Reservation(idAudience=2, idUser=3, idStatus=1,
                           amountOfHours=8, dateTimeOfReservation="26.10.2021", dateTimeOfEndReservation="27.11.2021")

with Session() as session:
    session.add(user1)
    session.add(audience1)
    session.add(status1)
    session.commit()
    session.add(reservation1)

    session.add(user2)
    session.add(status2)
    session.commit()
    session.add(reservation2)

    session.add(user3)
    session.add(audience2)
    session.commit()
    session.add(reservation3)
    session.commit()

print(session.query(User).all()[0])
