# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Example user database
users = {'user1': {'password': 'password1'}, 'user2': {'password': 'password2'}}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[username]['password']

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'></input>
                <input type='password' name='password' id='password' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    username = request.form['username']
    if request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id

if __name__ == '__main__':
    app.run(debug=True)
