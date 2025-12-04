from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from wtforms_components import TimeField
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"

class AlarmTime(FlaskForm):
    time = TimeField('Time', validators = [InputRequired()])
    submit = SubmitField("Set Alarm")

@app.route("/", methods = ["GET", "POST"])
def index():
    form = AlarmTime()
    if form.validate_on_submit():
        t = form.time.data
        #print(t)
        return f"Time the alarm will go off will be: {t}"
    return render_template("index.html", form = form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)