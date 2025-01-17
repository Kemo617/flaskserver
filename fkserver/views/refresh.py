
from fkserver import jsonify, Stock, app, login_required, current_user, getStockinfoSrcStatusDesc

# ...

# 响应页面的刷新请求
@app.route('/refresh_pagedata')
@login_required 
def refresh_data():
    data = {}

    try:      
        for stock in Stock.query.filter_by(username=current_user.username): 
            if stock.pricenow != 0.0:  
                data['#'+stock.stockcode] = (stock.pricenow, stock.getcolorclass())
        
        data['#status'] = getStockinfoSrcStatusDesc()
    except BaseException as e:
        pass
    
    return jsonify(data)