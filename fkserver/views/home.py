from fkserver import app, render_template, login_required

# ...

# 主页
@app.route('/')
@login_required 
def home():
    return render_template('home.html')