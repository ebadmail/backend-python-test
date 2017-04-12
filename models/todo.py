from alayatodo import connect_db as db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(120), unique=True)
    is_complete = db.Column(db.Integer, default=0)

    def __init__(self, user_id, description):
        self.user_id = user_id
        self.description = description

    def __repr__(self):
        return '<User %r>' % self.user_id 
