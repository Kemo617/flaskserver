from fkserver import app, db
from fkserver import Stock, send_inform_mail, get_users, getTimeNow

# ...

# 当前天类
class ResetTrigger():
    day = getTimeNow().day

    # 天的数值变化则可以重置
    @classmethod
    def isTimeToReset(cls):
        result = False
        
        newday = getTimeNow().day
        if newday != cls.day:
            cls.day = newday
            result = True

        return result

# 发送提醒邮件的任务, 定时执行
def sendinformEmails():
    try:
        flag_commit = False
        with app.app_context():
            for user in get_users():               
                stocks = []
                for stock in Stock.query.filter_by(username=user.username):
                    stocks.append(stock)
                flag_commit = flag_commit or send_inform_mail(user=user, stocks=stocks) 

            if ResetTrigger.isTimeToReset():
                for stock in Stock.query.all():
                    stock.resetinformedflags()
                db.session.commit() 
    except BaseException as e:
            pass    

