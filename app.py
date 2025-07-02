from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# Import other python files into the app
from models import db, User, Credential #imports the db models
from forms import LoginForm, RegisterForm, CredentialForm #imports what the user inserts to login
from config import Config #imports the configuration of the app
from encryption import encrypt_password, decrypt_password #imports the encryption of passwords
from generator import generate_password #imports the function to generate passwords

app = Flask(__name__)  # Starts the flask app
app.config.from_object(Config) #loads config into the app
db.init_app(app)  # starts the database


login_manager = LoginManager() #login manager for the flask page
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader # flask stores previous user IDs
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST']) #route for new users
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        # Create and save new user
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.')
        return redirect(url_for('login'))

    # show registration form
    return render_template('register.html', form=form)

@app.route('/', methods=['GET', 'POST']) #login route
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data): #checks if user exists and if the password exists
            login_user(user)  # Log in the user
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')  # Authentication failed

    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST']) #route if the user is logged in
@login_required
def dashboard():
    form = CredentialForm()
    # Handle new credential form submission
    if form.validate_on_submit():
        encrypted_pw = encrypt_password(form.password.data)
        cred = Credential(
            service=form.service.data,
            username=form.username.data,
            password_encrypted=encrypted_pw,
            user_id=current_user.id
        )
        db.session.add(cred)
        db.session.commit()
        return redirect(url_for('dashboard'))

    # Load and decrypt all saved credentials for the user
    credentials = Credential.query.filter_by(user_id=current_user.id).all()
    for c in credentials:
        c.password_plain = decrypt_password(c.password_encrypted)

    return render_template('dashboard.html', form=form, credentials=credentials)

@app.route('/logout') #gives the user the option to logout
@login_required
def logout():
    logout_user() #logouts the user
    return redirect(url_for('login')) #sends the user to login page

@app.route('/generate-password') #API route to generates random passwords
def generate_password_api():
    length = int(request.args.get('length', 12))
    use_digits = request.args.get('digits', '1') == '1'
    use_special = request.args.get('special', '1') == '1'
    # Generate a password based on options
    password = generate_password(length, use_digits, use_special)
    return jsonify({'password': password})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)  # Start flask server
