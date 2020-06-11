from mainblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    id = db.Column(db.String(20), unique=True, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    firstname = db.Column(db.String(60), nullable=True, default='')
    lastname = db.Column(db.String(60), nullable=True, default='')
    group = db.Column(db.String(60), db.ForeignKey('groups.group_name'), nullable=True)
    position = db.Column(db.String(60), db.ForeignKey('position.position_name'), nullable=True)
    comments = db.relationship('Comments', backref='author', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        if not self.firstname and not self.lastname:
            return f"{self.email}"
        else:
            return f"{self.firstname} {self.lastname}"


class Groups(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    group_name = db.Column(db.String(20), unique=True, nullable=False)
    members = db.relationship('User', backref='Group members', lazy=True)

    def __repr__(self):
        return f"{self.group_name}"

class Position(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    position_name = db.Column(db.String(20), unique=True, nullable=False)
    members = db.relationship('User', backref='Position members', lazy=True)
    def __repr__(self):
        return f"{self.position_name}"

class Comments(db.Model):
    id = db.Column(db.String(20), unique=True, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"(ID: {self.id})"

class Post(db.Model):
    id = db.Column(db.String(20), unique=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"(ID: {self.id}) \n {self.title}"