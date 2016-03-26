"""
OAI-PMH Validation oaipmh_validation_service

Work to replace https://www.openarchives.org/Register/ValidateSite

reCaptcha support based on flask-wtf example code from
https://github.com/lepture/flask-wtf/tree/master/examples/recaptcha
"""
from flask import Flask, render_template, flash, session, redirect, url_for, logging
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from flask.ext.wtf import Form
from flask.ext.wtf.recaptcha import RecaptchaField
import os.path

app = Flask(__name__)
logger = logging.create_logger(app) #FIXME - what is best way to set this up?
cfg = 'oaipmh_validation_service.cfg'
app.config.from_pyfile(cfg+'_default') #assume default always present
app.config.from_pyfile(cfg, silent=True) #override for real config

class ValidateForm(Form):

    base_url = TextAreaField("baseURL", validators=[DataRequired()])
    recaptcha = RecaptchaField()

@app.route("/")
def index():
    return redirect(url_for("validate"))

@app.route("/pmh/validate")
def validate(form=None):
    if form is None:
        form = ValidateForm()
    base_url = session.get("base_url", [])
    return render_template("validate.html",
                           base_url=base_url,
                           form=form)

@app.route("/pmh/validate/run", methods=("POST",))
def run_validate():
    form = ValidateForm()
    if form.validate_on_submit():
        session['base_url'] = form.base_url.data
        return render_template("validate_run.html",
                               base_url=form.base_url.data)
    else:
        # go back and try again...
        #logger.info("Invalid form entry, redirecting back")
        flash("Invalid form submission, please try again.")
        return redirect(url_for("validate"))

if __name__ == "__main__":
    app.run()
