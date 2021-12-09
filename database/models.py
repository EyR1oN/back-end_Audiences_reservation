from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, ForeignKey, VARCHAR

engine = create_engine('mysql+pymysql://root:password@localhost:3306/swagger_service')
engine.connect()

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

BaseModel = declarative_base()


class UserStatus(BaseModel):
    __tablename__ = "UserStatus"
    idStatus = Column(Integer, primary_key=True, autoincrement=True)
    statusName = Column(VARCHAR(45))


class User(BaseModel):
    __tablename__ = "User"
    idUser = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(VARCHAR(45))
    firstName = Column(VARCHAR(45))
    lastName = Column(VARCHAR(45))
    email = Column(VARCHAR(45))
    password = Column(VARCHAR(100))
    phoneNumber = Column(VARCHAR(45))
    userStatus = Column(Integer, ForeignKey(UserStatus.idStatus))


class Audience(BaseModel):
    __tablename__ = "Audience"
    idAudience = Column(Integer(), primary_key=True, autoincrement=True)
    number = Column(VARCHAR(45))


class StatusAudience(BaseModel):
    __tablename__ = "Status"
    idStatus = Column(Integer, primary_key=True, autoincrement=True)
    statusName = Column(VARCHAR(45))


class Reservation(BaseModel):
    __tablename__ = "Reservation"
    idReservation = Column(Integer, primary_key=True, autoincrement=True)
    idAudience = Column(Integer, ForeignKey(Audience.idAudience))
    idUser = Column(Integer, ForeignKey(User.idUser))
    idStatus = Column(Integer, ForeignKey(StatusAudience.idStatus))
    amountOfHours = Column(Integer)
    dateTimeOfReservation = Column(VARCHAR(45))
    dateTimeOfEndReservation = Column(VARCHAR(45))



