from fkserver import app, db, request, socketio, User, current_user

# ...

# 有客户端的主页连接到服务器
@socketio.on('client_connected')
def handle_event(data):
    # 保存到数据库
    if current_user is not None:
        random_send_id = data['random_send_id']
        current_user.random_send_id = random_send_id
        db.session.commit()
        # socketio.emit(random_send_id, {'message': random_send_id})

# 接收股票源端的数据并处理, 周期性接收
@app.route('/interface', methods=['POST'])
def interface():
    # 与股票信息源端的接口
    result = 'handle failed'
    
    try:
        message = request.get_json()
        data_type = message.pop('data_type')

        
        # 处理接收到的股票价格, 刷新数据库
        # 处理接收到的空心跳, 推动自动发送邮件任务

        # 处理4类包, 1.查询用户的股票列表, 返回列表; 2.列表中股票的信息, 返回ok; 3.心跳, 返回ok; 4.A股所有股票的名称和代码

        result = 'handle ok'
    except BaseException as e:
        pass

    return 'OK'