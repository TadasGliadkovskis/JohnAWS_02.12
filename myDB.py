from flask_sqlalchemy import SQLAlchemy

from .__init__ import db


class userTable(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    user_id = db.Column(db.Integer)
    authkey = db.Column(db.String())
    login = db.Column(db.Integer)
    read_access = db.Column(db.Integer)
    write_access = db.Column(db.Integer)

    def __init__(self, name, user_id, authkey, login, read_access, write_access):
        self.name = name
        self.user_id = user_id
        self.authkey = authkey
        self.login = login
        self.write_access = write_access
        self.read_access = read_access


    def delete_all(self):
        try:
            db.session.query(userTable).delete()
            db.session.commit()
            print("Delete all Done")
        except Exception as e:
            print("Failed " + str(e))
            db.session.rollback()


    def get_user_row_if_exists(self,user_id):
        get_user_row = userTable.query.filter_by(user_id=user_id).first()
        if (get_user_row != None):
            return get_user_row
        else:
            print("User does not exist")
            return False

    def add_user_and_login(self, name, user_id):
        row = self.get_user_row_if_exists(user_id)
        if row != False:
            row.login = 1
            db.session.commit()
        else:
            print("Adding new User " + name)
            new_user = userTable(name,user_id, None, 1, 0, 0)
            db.session.add(new_user)
            db.session.commit()
        print('user ' + name + " Login added")

    def user_logout(self, user_id):
        row = self.get_user_row_if_exists(user_id)
        if row != False:
            row.login = 0
            db.session.commit()
            print("User " + row.name + " Logged out")
        else:
            print("No such user")

"""
class plants(db.model):
    __tablename__ = "plants"
    plant_name = db.Column(db.String(), primary_key=True)
    ideal_lower_temperature = db.Column(db.Float)
    ideal_higher_temperature = db.Column(db.Float)
    ideal_humidity = db.Column(db.Integer)
    ideal_soil_moisture = db.Column(db.Integer)


class user_plant(db.model):
    __tablename__ = "user_plant"
    plant_id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(), primary_key=True, foreign_key=True)
    plant_name = db.Column(db.String, primary_key=True, foreign_key=True)
    watered = db.Column(db.Date)
    planted = db.Column(db.Date)

class plant_readings(db.model):
    __tablename__ = "plant_readings"
    plant_id = db.Column(db.String(), primary_key=True)
    raspi_id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(), primary_key = True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    soil_moisture = db.Column(db.Integer)
    reading_time = db.Column(db.TimeStamp(timezone=True))
"""

# NOW ADD METHODS TO ACCESS UPDATE and QUERY THE USERS TABLE