from fkserver import app, db, request, json, Stockbase, text

# ...

# 接收数据源端发来的信息
@app.route('/interface', methods=['POST'])
def handle_data_event():
    # 处理4类包, 1.查询用户的股票列表, 返回列表; 2.列表中股票的信息, 返回ok; 3.心跳, 返回ok; 4.A股所有股票的名称和代码
    result = 'ok'
    
    data = request.get_data()
    dict_data = json.loads(data)
    msgtype = dict_data['type']
    if msgtype == 'allstocks':
        dealallstocks(dict_data['data'])

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


