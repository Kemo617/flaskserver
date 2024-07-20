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
