from fkserver import app, db, request, json, Stock, Stockbase, text, sendinformEmails, jsonify, StockinfoSrcStatus

# ...

# 接收数据源端发来的信息
@app.route('/interface', methods=['POST'])
def handle_data_event():
    # 处理4类包, 1.查询用户的股票列表, 返回列表; 2.列表中股票的信息, 返回ok; 3.心跳, 返回ok; 4.A股所有股票的名称和代码
    result = 'ok'
    
    try:
        data = request.get_data()
        dict_data = json.loads(data)
        msgtype = dict_data['type']
        if msgtype == 'allstocks':
            # print('--- 收到所有股票名称和代码信息')
            dealallstocks(dict_data['data'])
        elif msgtype == 'checkselfstocks':
            StockinfoSrcStatus.renewserverstatus()
            # print('--- 收到查询所有用户自选股请求')
            result = dealcheckselfstocks()
            pass
        elif msgtype == 'selfstocks':
            # print('--- 收到所有用户自选股信息')
            dealselfstocks(dict_data['data'])
            pass
        elif msgtype == 'heartbeat':
            # print('--- 收到心跳')
            StockinfoSrcStatus.renewserverstatus()
            dealheartbeat()
            pass
    except BaseException as e:
        pass

    return result

# 处理接收到的所有股票名称和代码信息
def dealallstocks(dict):
    db.create_all()
    db.session.execute(text("DROP TABLE IF EXISTS stockbase"))
    db.create_all()

    for key, value in dict.items():
        stockbase = Stockbase()
        stockbase.stockcode = key
        stockbase.stockname = value
        db.session.add(stockbase)

    db.session.commit()

# 处理接收到的查询自选列表信息
def dealcheckselfstocks():
    # 充当心跳, 推动发送邮件任务
    sendinformEmails()

    # 组装列表信息, 发回去
    stockcodes = set()
    for stock in Stock.query.all():
        stockcodes.add(stock.stockcode)

    return jsonify(list(stockcodes))

# 处理接收到的自选列表信息
def dealselfstocks(dict):
    for stock in Stock.query.all():
        if stock.stockcode in dict.keys():
            pricesdict = dict[stock.stockcode]
            stock.pricenow = pricesdict['pricenow']
            stock.priceyesterday = pricesdict['priceyesterday']
    db.session.commit()

# 处理心跳
def dealheartbeat():
    # 推动定时任务
    sendinformEmails()
    pass


