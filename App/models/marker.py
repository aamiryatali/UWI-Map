from App.database import db

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x =  db.Column(db.Double, nullable=False)
    y = db.Column(db.Double, nullable=False)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_json(self):
        return{
            'x': self.x,
            'y': self.y
        }
