from fkserver import db

# ...

class Stockbase(db.Model):
        __tablename__ = "stockbase"
        id = db.Column(db.Integer, primary_key=True)
        stockcode = db.Column(db.String(20)) # 股票代码
        stockname = db.Column(db.String(20)) # 股票名称
