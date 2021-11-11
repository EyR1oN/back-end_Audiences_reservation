from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR

engine = create_engine('mysql+pymysql://root:qwerty@127.0.0.1/pp')
engine.connect()

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = "User"
    idUser = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(VARCHAR(45))
    firstName = Column(VARCHAR(45))
    lastName = Column(VARCHAR(45))
    email = Column(VARCHAR(45))
    password = Column(VARCHAR(100))
    phoneNumber = Column(VARCHAR(45))


class Audience(BaseModel):
    __tablename__ = "Audience"
    idAudience = Column(Integer(), primary_key=True, autoincrement=True)
    number = Column(VARCHAR(45))


class Status(BaseModel):
    __tablename__ = "Status"
    idStatus = Column(Integer, primary_key=True, autoincrement=True)
    statusName = Column(VARCHAR(45))


class Reservation(BaseModel):
    __tablename__ = "Reservation"
    idReservation = Column(Integer, primary_key=True, autoincrement=True)
    idAudience = Column(Integer, ForeignKey(Audience.idAudience))
    idUser = Column(Integer, ForeignKey(User.idUser))
    idStatus = Column(Integer, ForeignKey(Status.idStatus))
    amountOfHours = Column(Integer)
    dateTimeOfReservation = Column(VARCHAR(45))
    dateTimeOfEndReservation = Column(VARCHAR(45))


BaseModel.metadata.create_all(engine)
