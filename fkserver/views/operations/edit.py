from fkserver import app, redirect, url_for, request, render_template, login_required, current_user, Stock
# ...

# 打开编辑
@app.route('/stock/edit', methods=['POST'])
@login_required 
def edit():
    stockcode = request.form['stockcode']
    stocks = Stock.query.filter_by(username=current_user.username, stockcode=stockcode).all()
    stock = None
    if len(stocks) > 0:
        stock = stocks[0]

    return render_template('edit.html', stock=stock)