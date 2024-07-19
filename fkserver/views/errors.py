from fkserver import render_template, login_required, app
# ...

# 404错误页
@app.errorhandler(404)
@login_required 
def page_not_found(e):
    return render_template('404.html'), 404