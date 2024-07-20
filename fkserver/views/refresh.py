
from fkserver import jsonify, Stock, app, login_required, current_user, StockinfoSrcStatus

# ...

# 响应页面的刷新请求
@app.route('/refresh_pagedata')
@login_required 
def refresh_data():
    data = {}

    try:      
        status = '数据源在线'
        status_style = 'status-online'
        if not StockinfoSrcStatus.isStatusonline():
            status = '数据源离线'
            status_style = 'status-offline'

        for stock in Stock.query.filter_by(username=current_user.username):   
            print(f'--- 状态 {status_style}') 
            data['#'+stock.stockcode] = (stock.pricenow, stock.getcolorclass(), status, status_style)
    except BaseException as e:
        pass
    
    return jsonify(data)