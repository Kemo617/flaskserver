from fkserver import app, db
from fkserver import Stock, User, dt, pytz

# ...

# 获取当前时间
def getTimeNow():
    return dt.now(pytz.timezone('Asia/Shanghai'))


# 得到所有用户的自选股代码
def get_stockcodes_all():
    stockcodes = set()
    with app.app_context():
        for stock in Stock.query.all():
            stockcodes.add(stock.stockcode)
    return stockcodes 

# 得到某用户所有的个股代码
def get_stockcodes(username):
    stockcodes = []
    with app.app_context():
        for stock in Stock.query.filter_by(username=username):
            stockcodes.append(stock.stockcode)
    return stockcodes

# 得到所有用户
def get_users():
    users = []
    with app.app_context():
        users = User.query.all()
    return users

# 用新价格更新所有用户名下的该支股票
def update_stockprices(stockcode, prices):
    with app.app_context():
        for stock in Stock.query.filter_by(stockcode=stockcode):
            stock.pricenow = prices[0]
            stock.priceyesterday = prices[1]
            db.session.commit()

# 得到某用户的随机发送id
def get_send_id(username):
    random_send_id = ''
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user is not None:
            random_send_id = user.random_send_id
    return random_send_id