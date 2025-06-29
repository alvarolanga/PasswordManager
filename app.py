from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Credential
from forms import LoginForm, RegisterForm, CredentialForm
from config import Config
from encryption import encrypt_password, decrypt_password
from generator import generate_password

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = CredentialForm()
    if form.validate_on_submit():
        encrypted_pw = encrypt_password(form.password.data)
        cred = Credential(service=form.service.data,
                          username=form.username.data,
                          password_encrypted=encrypted_pw,
                          user_id=current_user.id)
        db.session.add(cred)
        db.session.commit()
        return redirect(url_for('dashboard'))
    credentials = Credential.query.filter_by(user_id=current_user.id).all()
    for c in credentials:
        c.password_plain = decrypt_password(c.password_encrypted)
    return render_template('dashboard.html', form=form, credentials=credentials)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/generate-password')
def generate_password_api():
    length = int(request.args.get('length', 12))
    use_digits = request.args.get('digits', '1') == '1'
    use_special = request.args.get('special', '1') == '1'
    password = generate_password(length, use_digits, use_special)
    return jsonify({'password': password})



# ✅ Only keep this block once:
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
