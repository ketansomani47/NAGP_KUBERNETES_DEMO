from flask import Flask
from flask import jsonify, make_response, request, session
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from urllib.parse import quote_plus
import os

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = quote_plus(os.environ["DB_PASSWORD"])
DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

db = SQLAlchemy(app)


class UserProfile(db.Model):
    __tablename__ = "UserProfile"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=True)


class UserProfileSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    age = fields.Integer()


single_user = UserProfileSchema()
multi_user = UserProfileSchema(many=True)


@app.route("/", methods=["GET"])
def get_status():
    try:
        return make_response(jsonify({"message":"Server Running..."}),200)
    except Exception as e:
        print("exception:", str(e))
        return make_response(jsonify({"message": "error occurred while getting data "+str(e)}),500)


@app.route("/get_user", methods=["GET"])
def get_user_detail():
    try:
        users = UserProfile.query.all()
        user_data = multi_user.dump(users)
        if len(user_data) > 0:
            return make_response(jsonify({"message": "User List", "Data": user_data}), 200)
        return make_response(jsonify({"message": "No data found"}), 204)
    except Exception as e:
        print("exception:", str(e))
        return make_response(jsonify({"message": "error occurred while getting data "+str(e)}), 500)


@app.route("/add_user", methods=["POST"])
def post_user_detail():
    try:
        if request.get_json():
            data = request.get_json()
        elif request.form:
            data = request.form
        elif request.args:
            data = request.args
        else:
            return make_response(jsonify({"message": "data is missing"}), 400)
        invalidate_user = single_user.validate(data)
        if invalidate_user:
            return make_response(jsonify({"message":invalidate_user}),400)
        user = UserProfile()
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.age = data["age"] if "age" in data.keys() else None
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"message": "user added successfully"}), 200)
    except Exception as e:
        print("exception:", str(e))
        return make_response(jsonify({"message":"error occurred while getting data "+str(e)}), 500)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000, host="0.0.0.0")
