from fkserver import app, db, request, socketio, User, current_user, json, Stockbase, text

# ...

# 有客户端的主页连接到服务器
@socketio.on('client_connected')
def handle_connect_event(data):
    # 保存到数据库
    if current_user is not None:
        random_send_id = data['random_send_id']
        current_user.random_send_id = random_send_id
        db.session.commit()
        # socketio.emit(random_send_id, {'message': random_send_id})

# 接收股票源端的数据并处理, 周期性接收
@socketio.on('stock_data')
def handle_data_event(data):
    # 处理接收到的股票价格, 刷新数据库
    # 处理4类包, 1.查询用户的股票列表, 返回列表; 2.列表中股票的信息, 返回ok; 3.心跳, 返回ok; 4.A股所有股票的名称和代码
    dict_data = json.loads(data)
    msgtype = dict_data['type']
    if msgtype == 'singlestock':
        pass
    elif msgtype == 'allstocks':
        dealallstocks(dict_data['data'])

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


