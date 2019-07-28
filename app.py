from flask import Flask, request, jsonify
from flask_expects_json import expects_json
from src.entitys.entity import Session, engine, Base
from src.entitys.entity import Entity
from src.entitys.entity import EntitySchema
from src.password.passwordGenerator import PasswordGenerator
from src.have_i_been_pawnd.checkAccount import check_email, check_password

Base.metadata.create_all(engine)

app = Flask(__name__)

new_pass_schema = {

    "properties": {
        "user_id": {"type": "int"},
        "safe_pass_id": {"type": "int"},
        "name": {"type": "string"},
        "login": {"type": "string"},
        "password": {"type": "string"},
        "e_mail": {"type": "string"},
        "website": {"type": "string"},
        "note": {"type": "string"}
    },
    "required": ["user_id", "safe_pass_id", "name", "login", "password", "e_mail", "website", "note"]
}

new_password_schema = {

    "properties": {
        "min_upper_chars": {"type": "int"},
        "min_lower_chars": {"type": "int"},
        "min_numbers": {"type": "int"},
        "min_special_chars": {"type": "int"},
        "start_password_with_upper": {"type": "boolean"},
        "pass_length": {"type": "int"}
    },
    "required": ["min_upper_chars", "min_lower_chars", "min_numbers", "min_special_chars", "start_password_with_upper",
                 "pass_length"]
}


@app.route('/new_pass', methods=["POST"])
@expects_json(new_pass_schema)
def new_pass():
    """
    :description: Takes user_id as input safes new SafePass in DB
                  Returns status 201 if saving was successful.
                  Returns status 400 if json is not correct.
                  Returns status 500 if status was not successful.
    :param: takes json from request.
            Json (must *) contain:
                user_id  : int *
                safe_pass_id: int
                name     : string *
                login    : string *
                password : string *
                e_mail   : string / none
                website  : string / none
                note     : string / none

    :return: status code
    """

    data = request.json

    safe_pass = Entity(user_id=data["user_id"],
                       safe_pass_id=data["safe_pass_id"],
                       name=data["name"],
                       login=data["login"],
                       password=data["password"],
                       e_mail=data["e_mail"],
                       website=data["website"],
                       note=data["note"]
                       )

    # get all safepasses in db
    # if safepass_id in db then update object
    # if not then save as new

    # noinspection PyBroadException
    try:
        session = Session()
        session.add(safe_pass)
        session.commit()
        session.close()

        response = app.response_class(status=201)
        return response
    except Exception as exception:
        response = app.response_class(status=500, response="Error occurred while" + str(exception))
        return response


@app.route("/get_pass_specific", methods=["GET"])
def get_pass_specific():
    session = Session()

    # TODO If none raise error
    specific_safe_pass_id = request.args.get("safe_pass_id")

    safe_pass_objects = session.query(Entity).filter_by(Entity.safe_pass_id == specific_safe_pass_id)

    # transforming into JSON-serializable objects
    schema = EntitySchema(many=True)
    safe_passes = schema.dump(safe_pass_objects)

    session.close()

    response = app.response_class(status=200, response=jsonify(safe_passes.data), content_type="application/json")
    return response


@app.route("/get_pass_user", methods=["GET"])
def get_pass_user():
    session = Session()

    specific_user_id = request.args.get("user_id")

    safe_pass_objects = session.query(Entity).filter_by(Entity.user_id == specific_user_id)

    # transforming into JSON-serializable objects
    schema = EntitySchema(many=True)
    safe_passes = schema.dump(safe_pass_objects)

    session.close()

    response = app.response_class(status=200, response=jsonify(safe_passes.data), content_type="application/json")
    return response


@app.route("/delete_pass", methods=["DELETE"])
def delete_pass():
    session = Session()

    specific_safe_pass_id = request.args.get("safe_pass_id")
    session.delete(specific_safe_pass_id)

    session.close()

    response = app.response_class(status=200)
    return response


@app.route("/get_pass", methods=["GET"])
@expects_json(new_pass_schema)
def get_password():
    session = Session()

    data = request.json

    pwd = PasswordGenerator(
        data["min_upper_chars"],
        data["min_lower_chars"],
        data["min_numbers"],
        data["min_special_chars"],
        data["start_with_password_upper"],
        data["password_length"]
    )
    password = pwd.generate_password()

    session.close()

    response = app.response_class(status=200, response="{password:" + password + "}", content_type="application/json")
    return response


@app.route("/check_password", methods=["GET"])
def check_password():
    password = request.args.get("password")

    if check_password(password):
        response = app.response_class(status=200, response="{password_found:" + str(True) + "}",
                                      content_type="application/json")
        return response

    response = app.response_class(status=200, response="{password_found:" + str(False) + "}",
                                  content_type="application/json")
    return response


@app.route("/check_email", methods=["GET"])
def check_email():
    email = request.args.get("email")

    if check_email(email) is False:
        response = app.response_class(status=200, response="{email_found:" + str(False) + "}",
                                      content_type="application/json")
        return response

    response = app.response_class(status=200,
                                  response="{email_found:" + str(True) + "breaches:" + check_email(email) + "}",
                                  content_type="application/json")
    return response


@app.route("/user_checkin", methods=["GET"])
def user_checkin():
    user_name = request.args.get("user_name")
    user_pass = request.args.get("user_pass")

    #If user in db then send back user id, 200
    #if user not in db send 404

if __name__ == '__main__':
    app.run()
