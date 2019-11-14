from flask import Flask, request, Response, render_template
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Regexp
import re

class WordForm(FlaskForm):
    avail_letters = StringField("Letters", validators= [
        Regexp(r'^[a-z]+$', message="must contain letters only")
    ])
    submit = SubmitField("Go")


csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)

@app.route('/')
def index():
    form = WordForm()
    return render_template("/templates/index.html", form=form)

