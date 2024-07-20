from fkserver import getTimeNow, datetime, pytz

# ...

# 当前股票数据源状态类
class StockinfoSrcStatus():
    lastRecTime = datetime(2000, 1, 1, 1, 1, 1, 1, tzinfo=pytz.timezone('Asia/Shanghai'))

    # 分钟数值变化则可以发送
    @classmethod
    def isStatusonline(cls):
        result = False

        # 当前时间比上次更新时间小于30秒, 则判断数据源没断
        shanghaiTime = getTimeNow()
        interval = shanghaiTime - cls.lastRecTime
        if interval.seconds < 30:
            result = True

        return result
    
    @classmethod
    def renewserverstatus(cls):
        cls.lastRecTime = getTimeNow()

# 获取股票数据源的当前状态描述
def getStockinfoSrcStatusDesc():
    status = '数据源在线'
    status_style = 'status-online'
    if not StockinfoSrcStatus.isStatusonline():
        status = '数据源离线'
        status_style = 'status-offline'
    
    return (status, status_style)
