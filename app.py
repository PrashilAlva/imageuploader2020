from flask import Flask, render_template, redirect, request, session, flash
import datetime
import jwt
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address
)

app.config['SECRET_KEY'] = "ALeKk01Zi5-u5XqSe44zsBSuemEZ4Sv44g%3A1607399389200&ei=3ffOX7_OC4WLmgfqv7DoDw"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = session['access']
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
            except:
                flash('Token Expired / Invalid, Kindly Login again.', 'warning')
                sess = session.pop('access')
                return redirect('/login')
        except:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated


@app.route('/', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
@token_required
def home():
    result = False
    if request.method == "POST":
        result = True
        name = request.form['fileName']
        return render_template('index.html', name=name, result=result)
    return render_template('index.html', result=result)


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    try:
        if session['access']:
            return redirect('/')
    except:
        pass
    if request.method == "POST":
        uname = request.form['uname']
        pword = request.form['pword']
        if uname == "prashil" and pword == "secret":
            token = jwt.encode({'user': uname, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=1)}, app.config['SECRET_KEY'])
            session['access'] = token.decode('UTF-8')
            return redirect('/')
        flash('Invalid Credentials!', 'error')
        return render_template('login.html')
    return render_template('login.html')

if __name__ == "__main__":
    app.run(port=4200, debug=False)
