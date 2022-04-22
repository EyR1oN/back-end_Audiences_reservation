from flask import Flask, Response
from models import *
from flask import jsonify
import json
from functools import wraps
from flask import make_response
from flask import request
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
bcrypt = Bcrypt(app)
idres = None


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        user_ = Session.query(User).filter_by(username=auth.username).first()
        if auth and user_ and bcrypt.check_password_hash(user_.password, auth.password):
            return f(*args, **kwargs)

        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated


def auth_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        user_ = Session.query(User).filter_by(username=auth.username).first()
        if auth and user_ and bcrypt.check_password_hash(user_.password, auth.password):
            userStatus_ = Session.query(UserStatus).filter_by(statusName='SuperUser').first()
            if user_.userStatus == userStatus_.idStatus:
                return f(*args, **kwargs)
            else:
                return make_response('You are not allowed!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated


def to_json(inst, cls):
    convert = dict()
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:  # pragma: no cover
                d[c.name] = convert[c.type](v)
            except:  # pragma: no cover
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
        return make_response(jsonify({'error': 'Not found'}), 401)


@app.route('/user/<string:username>', methods=['DELETE'])
@auth_admin
def delete_user(username):
    try:
        user = Session.query(User).filter_by(username=username).first()
        reservation = Session.query(Reservation).filter_by(idUser=user.idUser).all()
        for i in reservation:  # pragma: no cover
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
        password=bcrypt.generate_password_hash(request.json.get('password')),
        phoneNumber=request.json.get('phoneNumber'),
        userStatus=request.json.get('userStatus')
    )
    tvins = Session.query(User).filter_by(username=user.username).all()
    if tvins:
        return make_response(jsonify({'error': 'username is taken'}), 409)
    try:  # pragma: no cover
        Session.add(user)
        Session.commit()
    except IntegrityError:
        return make_response(jsonify({'error': 'incorrect data'}), 409)
    a = to_json(user, User)
    return Response(response=a,
                    status=200,
                    mimetype="application/json")


@app.route('/user/<string:username>', methods=['PUT'])
@auth_admin
def update_user(username):
    u = Session.query(User).filter_by(username=username).first()
    if not u:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if request.json.get('username'):
        tvins = (Session.query(User).filter_by(username=request.json.get('username')).all())
        if tvins:
            return make_response(jsonify({'error': 'username is taken'}), 409)
        u.username = request.json.get('username')  # pragma: no cover
    if request.json.get('firstName'):
        u.firstName = request.json.get('firstName')  # pragma: no cover
    if request.json.get('lastName'):
        u.lastName = request.json.get('lastName')  # pragma: no cover
    if request.json.get('email'):
        u.email = request.json.get('email')  # pragma: no cover
    if request.json.get('password'):
        u.password = request.json.get('password')  # pragma: no cover
    if request.json.get('phoneNumber'):
        u.phoneNumber = request.json.get('phoneNumber')  # pragma: no cover
    if request.json.get('userStatus'):
        u.userStatus = request.json.get('userStatus')  # pragma: no cover
    Session.commit()

    return Response(response=to_json(u, User),
                    status=200,
                    mimetype="application/json")


# reservation

@app.route('/reservation', methods=['POST'])
@auth_required
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
@auth_required
def update_reservation(id):
    u = Session.query(Reservation).filter_by(idReservation=id).first()
    if not u:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if request.json.get('idAudience'):
        u.idAudience = request.json.get('idAudience')  # pragma: no cover
    if request.json.get('idUser'):
        u.idUser = request.json.get('idUser')  # pragma: no cover
    if request.json.get('idStatus'):
        u.idStatus = request.json.get('idStatus')  # pragma: no cover
    if request.json.get('amountOfHours'):
        u.amountOfHours = request.json.get('amountOfHours')  # pragma: no cover
    if request.json.get('dateTimeOfReservation'):
        u.dateTimeOfReservation = request.json.get('dateTimeOfReservation')  # pragma: no cover
    if request.json.get('dateTimeOfEndReservation'):
        u.dateTimeOfEndReservation = request.json.get('dateTimeOfEndReservation')  # pragma: no cover
    Session.commit()

    return Response(response=to_json(u, Reservation),
                    status=200,
                    mimetype="application/json")


@app.route("/reservation/<int:id>", methods=['GET'])
@auth_required
def get_reservation(id):
    try:
        a = to_json(Session.query(Reservation).filter_by(idReservation=id).one(), Reservation)
        return Response(response=a,
                        status=200,
                        mimetype="application/json")
    except:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/reservation/<int:id>', methods=['DELETE'])
@auth_admin
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
    app.run(debug=True)  # pragma: no cover
