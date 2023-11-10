from flask import Flask, render_template, request, redirect
import re
import time

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
app = Flask(__name__)

@app.route("/")
def index():
    # if there is an existing email parameter pass it through to the
    # template to focus it and select it
    email = request.args.get('email')
    if email is None:
        email = ""
    return render_template('index.j2', email=email)


@app.route("/thank-you")
def thankyou():
    return render_template('index.j2', thank_you=True)


@app.route("/signup", methods=["POST"])
def signup():

    # pause for 2 seconds
    time.sleep(2)

    # validate email
    email = request.form['email']
    error = None
    if email == "bad@email.com":
        error = "Spam Email"
    elif not re.fullmatch(email_regex, email):
        error = "Bad Email address"

    # handle htmx requests
    if request.headers.get('HX-Request'):
        if error:
            # re-render form on error
            return render_template('form.j2', email=email, error=error)
        else:
            # otherwise render the thank you element
            return render_template('thank_you.j2', email=email)
    else:
        # handle javascript-disabled requests
        if error:
            return render_template('index.j2', error=error, email=email)
        else:
            return redirect("/thank-you", code=303)



