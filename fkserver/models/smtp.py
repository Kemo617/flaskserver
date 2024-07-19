from fkserver import db

# ...

class SMTP(db.Model):
        __tablename__ = "smtp"
        id = db.Column(db.Integer, primary_key=True)
        server = db.Column(db.String(128))
        sendername = db.Column(db.String(20))
        senderaddress = db.Column(db.String(128))
        password = db.Column(db.String(128))