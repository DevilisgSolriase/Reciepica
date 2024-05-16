from __init__ import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='images.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # Changed 'post' to 'posts'
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_post = db.Column(db.String(20), nullable=False, default='images.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Changed 'user.id' to 'User.id'
    
    def __repr__(self):
        return f"Post('{self.title}')"    
