from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ce4551f3b39648f09badedd1beb7dbcf'


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # token = request.args.get('token')

        # Modification # 1 (Access the token from the header request)
        if 'token' in request.headers:  
          token = request.headers['token']

        if not token:
            return jsonify({'Alert!': 'Token is missing!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Alert!': 'Invalid Token!'})

        # Modification # 2 
        return func( *args,  **kwargs)

    return decorated


#Lets create our first route. the welcome route 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently'


@app.route('/public')
def public():
    return 'For public'

#Authenticated
@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome !!'




#I want to enter my username and password and once i have that 
# i will get the token KEY. that will mean i will logged in using JWT not a cookie        
# lets have another route for login

@app.route('/login', methods=['POST'])
def login():
    #Verify the username and password if its correct or not 
    if request.form['username'] and request.form['password'] == '12345':
        #Set session to true 
        session['logged-in'] = True

        #And Now encode the token for the user !!
        token = jwt.encode({'user':request.form['username'],
                            'expiration': str(datetime.utcnow()+timedelta(seconds=120))
                            },app.config['SECRET_KEY'])
        
        return jsonify({'taken': token.decode('utf-8')})
    else: 
        return make_response('Unable to verify', 403, {'www-Authenticate' : 'Basic realm:"Authentication Faild!"'})


if __name__ == "__main__":
    app.run(debug=True)

