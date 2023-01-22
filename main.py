from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps


app = Flask(__name__)
app.config["SECRET_KEY"] = "WebsiteMadeByWebLaunch2022"


# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

class Event(db.Model):
    __tablename__ = "Events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.Text)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)

class Gallery(db.Model):
    __tablename__ = "Gallery"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, nullable=False)

db.create_all()

# Login Manager

login_manager = LoginManager()
login_manager.init_app(app)

def is_admin():
    users_id = [1, 2, 3]
    if current_user.id not in users_id:
        return False
    else:
        return True

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if not is_admin():
                return abort(403)
            return f(*args, **kwargs)      
        except:
              return abort(403)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Routes
@app.route("/")
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)

@app.route("/about")
def about():
    return render_template("aboutus.html", logged_in=current_user.is_authenticated)

@app.route("/volunteer")
def volunteer():
    return render_template("vol.html", logged_in=current_user.is_authenticated)

@app.route("/contact")
def contact():
    return render_template("contactus.html", logged_in=current_user.is_authenticated)

@app.route("/donate")
def donate():
    return render_template("donateform.html", logged_in=current_user.is_authenticated)

# Events section
@app.route("/events")
def events():
    events = Event.query.all()
    try:
        admin = is_admin()
    except:
        admin = False
    return render_template("events.html", all_events=events,logged_in=current_user.is_authenticated, is_admin=admin)

@app.route("/add-event", methods=["GET", "POST"])
@admin_only
def add_event():
    if request.method == "POST":
        image =  request.files["image"]
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        description = request.form.get("description")

        new_event = Event(
            title=title,
            subtitle=subtitle,
            image=image.read(),
            description=description,
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Event added Successfully!")

    return render_template("add_event.html", logged_in=current_user.is_authenticated)

@app.route("/event-image/<int:id>")
def event_image(id):
    event = Event.query.get(id)
    image = event.image
    return app.response_class(image, mimetype='application/octet-stream')

@app.route("/event-update/<int:id>", methods=["GET", "POST"])
def event_update(id):
    event = Event.query.get(id)
    if request.method == "POST":
        event.title = request.form.get("title")
        event.subtitle = request.form.get("subtitle")
        event.description = request.form.get("description")
        if request.files["image"]:
            event.image =  request.files["image"].read()
        db.session.commit()
        print("hello")
        return redirect(url_for("events"))
    
    return render_template("update_event.html", event=event)

@app.route("/event-delete/<int:id>")
def event_delete(id):
    event = Event.query.get(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("events"))

# Gallery Section
@app.route("/gallery")
def gallery():
    gallery = Gallery.query.all()
    try:
        admin = is_admin()
    except:
        admin = False
    return render_template("gallery.html", gallery=gallery, logged_in=current_user.is_authenticated, is_admin=admin)

@app.route("/gallery-image/<int:id>")
def gallery_image(id):
    gallery_row = Gallery.query.get(id)
    image = gallery_row.image
    return app.response_class(image, mimetype="application/octet-stream")

@app.route("/add-gallery-image", methods=["GET", "POST"])
def add_gallery_image():
    if request.method == "POST":
        image = request.files["image"]
        new_image = Gallery(
            image = image.read(),
        )
        db.session.add(new_image)
        db.session.commit()
        flash("Image added successfully!")

    return render_template("add_gallery_image.html", logged_in=current_user.is_authenticated)

@app.route("/delete-image/<int:id>")
@admin_only
def delete_image(id):
    image = Gallery.query.get(id)
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for("gallery"))


# User login part
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")

        if User.query.filter_by(email=email).first():
            flash("User already registered, Please login instead!")
            return redirect(url_for('login'))

        name, password = request.form.get("name"), request.form.get("password")
        new_user = User(
            name = name,
            email = email,
            password = password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template("register.html", logged_in=current_user.is_authenticated)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            password = request.form.get("password")
            if user.password == password:
                login_user(user)
                return redirect(url_for("home"))

            flash("Invalid password")
            return redirect(url_for("login"))

        flash("User not registered with email!")
        return redirect(url_for("login"))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8080)
