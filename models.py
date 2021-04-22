from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)



class Disc(db.Model):
    """Disc Model"""

    __tablename__ = "discs"

    id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)

    name = db.Column(db.Text, 
                    nullable=False)

    plastic = db.Column(db.Text, 
                    default="N/A")

    disc_type = db.Column(db.Text)

    difficulty = db.Column(db.Float)

    speed = db.Column(db.Float)

    glide = db.Column(db.Float)

    turn = db.Column(db.Float)

    fade = db.Column(db.Float)

    image_url = db.Column(db.Text)

    company_name = db.Column(db.Text, 
                    db.ForeignKey('companies.name'))
                    

    company = db.relationship('Company', backref='discs')

    def __repr__(self):
        return f"<Disc: {self.name} Company: {self.company_name}>"

    def serialize(self):
        serialized = {
                    "name": self.name,
                    "plastic": self.plastic, 
                    "disc_type": self.disc_type, 
                    "difficulty": self.difficulty,
                    "speed": self.speed,
                    "glide": self.glide,
                    "turn": self.turn,
                    "fade": self.fade,
                    "company_name": self.company_name
                    }
        return serialized


class Company(db.Model):
    """Company Model"""

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    

    def __repr__(self):
        return f"<Company {self.name}>"

    def serialize(self):
        serialized = {"name": self.name}
        return serialized

