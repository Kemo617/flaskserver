from fkserver import db

# ...

class Stock(db.Model):
        __tablename__ = "stocks"
        id = db.Column(db.Integer, primary_key=True)
        stockcode = db.Column(db.String(20)) # 股票代码
        stockname = db.Column(db.String(20)) # 股票名称
        username = db.Column(db.String(20)) # 所属用户名
        pricenow = db.Column(db.Float) # 当前价格
        priceyesterday = db.Column(db.Float) # 昨日收盘价
        pricemaxset = db.Column(db.Float)
        priceminset = db.Column(db.Float)
        flag_max_informed = db.Column(db.Boolean)
        flag_min_informed = db.Column(db.Boolean)
        flag_is_informing = db.Column(db.Boolean)

        def __init__(self):
            # 设置的高提示价格
            self.pricemaxset = 0.0
            # 设置的低提示价格
            self.priceminset = 0.0
            # 发送标识
            self.flag_max_informed = False
            self.flag_min_informed = False
            # 是否发送
            self.flag_is_informing = False

            self.pricenow = 0.0
            self.priceyesterday = 0.0

        # 重置发送标识, 每天至少自动重置一次
        def resetinformedflags(self):
            self.flag_max_informed = False
            self.flag_min_informed = False

        # 判断当前股价跟上一交易日比, 涨还是跌
        def getcolorclass(self):
            result = "labelstockpriceBlack"
            if self.pricenow > self.priceyesterday:
                result = "labelstockpriceRed"
            elif self.pricenow < self.priceyesterday:
                result = "labelstockpriceGreen"

            return result