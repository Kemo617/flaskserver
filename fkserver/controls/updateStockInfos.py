from fkserver import get_stockcodes_all, update_stockprices, getTimeNow, getStockPrices

# ...

# 当前分钟类
class UpdateTrigger():
    minuteNow = -1

    # 分钟数值变化则可以发送
    @classmethod
    def isTimeToUpdate(cls):
        result = False

        # 每天北京时间9:29到15:01任务执行 周六日除外
        shanghaiTime = getTimeNow()
        weekday = shanghaiTime.today().weekday()
        startTime = getTimeNow().replace(hour=9, minute=29, second=0)
        endTime = getTimeNow().replace(hour=15, minute=1, second=0)
        if weekday != 6 and weekday != 7 and (startTime <= shanghaiTime <= endTime):     
            # 如果分钟数值变化了, 则可以更新
            result = False if cls.minuteNow == shanghaiTime.minute else True 

        cls.minuteNow = shanghaiTime.minute
        return result

# 更新股票价格信息任务, 定时执行
def updateStockInfos():
    try:
        if UpdateTrigger.isTimeToUpdate():
            # 把所有用户的stockcode收集到一个set中, 然后查询更新所有的股票价格信息
            for stockcode in get_stockcodes_all():
                prices = getStockPrices(stockcode=stockcode)
                # 更新每位用户名下的该支股票
                update_stockprices(stockcode=stockcode, prices=prices)

    except BaseException as e:
        print(f"定时更新股票价格任务异常 --> {e}")

