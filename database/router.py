from flask import Flask, Response
from models import *
from flask import jsonify
import json
from flask import make_response
from flask import request
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
bcrypt = Bcrypt(app)


def to_json(inst, cls):
    convert = dict()
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)


@app.route("/user/<string:username>", methods=['GET'])
def get_user(username):
    try:
        a = to_json(Session.query(User).filter_by(username=username).one(), User)
        return Response(response=a,
                        status=200,
                        mimetype="application/json")
    except:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/user/<string:username>', methods=['DELETE'])
def delete_user(username):
    try:
        user = Session.query(User).filter_by(username=username).first()
        reservation = Session.query(Reservation).filter_by(idUser=user.idUser).all()
        for i in reservation:
            Session.delete(i)
        Session.delete(user)
        Session.commit()
        return {
            "msg": "user deleted successfully",
            "id": username
        }
    except:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/user', methods=['POST'])
def create_user():
    user = User(
        username=request.json.get('username'),
        firstName=request.json.get('firstName'),
        lastName=request.json.get('lastName'),
        email=request.json.get('email'),
        password=bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8'),
        phoneNumber=request.json.get('phoneNumber')
    )
    tvins = Session.query(User).filter_by(username=user.username).all()
    if tvins:
        return make_response(jsonify({'error': 'username is taken'}), 409)
    try:
        Session.add(user)
        Session.commit()
    except IntegrityError:
        return make_response(jsonify({'error': 'incorrect data'}), 409)
    a = to_json(user, User)
    return Response(response=a,
                    status=200,
                    mimetype="application/json")


@app.route('/user/<string:username>', methods=['PUT'])
def update_user(username):
    u = Session.query(User).filter_by(username=username).first()
    if not u:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if request.json.get('username'):
        tvins = (Session.query(User).filter_by(username=request.json.get('username')).all())
        if tvins:
            return make_response(jsonify({'error': 'username is taken'}), 409)
        u.username = request.json.get('username')
    if request.json.get('firstName'):
        u.firstName = request.json.get('firstName')
    if request.json.get('lastName'):
        u.lastName = request.json.get('lastName')
    if request.json.get('email'):
        u.email = request.json.get('email')
    if request.json.get('password'):
        u.password = request.json.get('password')
    if request.json.get('phoneNumber'):
        u.phoneNumber = request.json.get('phoneNumber')
    Session.commit()

    return Response(response=to_json(u, User),
                    status=200,
                    mimetype="application/json")


@app.route('/reservation', methods=['POST'])
def create_reservation():
    reservation = Reservation(
        idAudience=request.json.get('idAudience'),
        idUser=request.json.get('idUser'),
        idStatus=request.json.get('idStatus'),
        amountOfHours=request.json.get('amountOfHours'),
        dateTimeOfReservation=request.json.get('dateTimeOfReservation'),
        dateTimeOfEndReservation=request.json.get('dateTimeOfEndReservation')
    )
    try:
        Session.add(reservation)
        Session.commit()
    except IntegrityError:
        return make_response(jsonify({'error': 'incorrect data'}), 409)
    a = to_json(reservation, Reservation)
    return Response(response=a,
                    status=200,
                    mimetype="application/json")


@app.route('/reservation/<int:id>', methods=['PUT'])
def update_reservation(id):
    u = Session.query(Reservation).filter_by(idReservation=id).first()
    if not u:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if request.json.get('idAudience'):
        u.username = request.json.get('idAudience')
    if request.json.get('idUser'):
        u.firstName = request.json.get('idUser')
    if request.json.get('idStatus'):
        u.lastName = request.json.get('idStatus')
    if request.json.get('amountOfHours'):
        u.amountOfHours = request.json.get('amountOfHours')
    if request.json.get('dateTimeOfReservation'):
        u.dateTimeOfReservation = request.json.get('dateTimeOfReservation')
    if request.json.get('dateTimeOfEndReservation'):
        u.dateTimeOfEndReservation = request.json.get('dateTimeOfEndReservation')
    Session.commit()

    return Response(response=to_json(u, Reservation),
                    status=200,
                    mimetype="application/json")


@app.route("/reservation/<int:id>", methods=['GET'])
def get_reservation(id):
    try:
        a = to_json(Session.query(Reservation).filter_by(idReservation=id).one(), Reservation)
        return Response(response=a,
                        status=200,
                        mimetype="application/json")
    except:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/reservation/<int:id>', methods=['DELETE'])
def delete_reservation(id):
    try:
        reservation = Session.query(Reservation).filter_by(idReservation=id).first()
        Session.delete(reservation)
        Session.commit()
        return {
            "msg": "reservation deleted successfully",
            "id": id
        }
    except:
        return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(debug=True)
