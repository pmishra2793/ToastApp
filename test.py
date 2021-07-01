# Only Testing Purpose - trying with mongoengine

from flask import Flask
from flask_mongoengine import MongoEngine
import mongoengine as me

class Movie(me.Document):
    title = me.StringField(required=True)
    year = me.IntField()
    rated = me.StringField()
    director = me.StringField()
    actors = me.ListField()

class MenuManagement(me.Document):
    menu_id = me.IntField(required=True)
    menu_name = me.StringField()                                              

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "toastApp",
}
db = MongoEngine(app)

def Menu():
    try:
        menu_id = 1
        menu_name = 'Samosa'
        menu = MenuManagement(menu_id=menu_id, menu_name=menu_name)
        menu.save()
    except Exception as e:
        print(str(e))

Menu()
