from fkserver import render_template, redirect, request, flash, url_for
from fkserver import FlaskForm, StringField, PasswordField, SubmitField, DataRequired, Length
from fkserver import User, login_required, login_user, logout_user
from fkserver import send_confirm_mail
from fkserver import app, db

# ...

# 定义表单模型类
class LoginForm(FlaskForm):
    # DataRequired 验证不为空, Length 限制长度
    username = StringField(label=u"用户名", validators=[DataRequired(), Length(min=0, max=18)])
    password = PasswordField(label=u"密码", validators=[DataRequired(), Length(min=0, max=18)])
    submitlogin = SubmitField(label=u"登入")

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user is not None:
                if user.validate_password(password):
                    if user.is_activated:
                        login_user(user)
                        flash(u"已登入.")
                        return redirect(url_for('home'))
                    else:
                        if send_confirm_mail(user):
                            flash(u"注册确认邮件已再次发送.")
                            db.session.commit()
                else:
                    flash(u"密码错误.")
            else:
                flash(u"用户未注册. 请留意大小写.")
        else:
            flash(u"无效输入.")

    return render_template('login.html', form=form)

# 登出
@app.route('/logout')
@login_required # 视图保护
def logout():
    logout_user()
    flash(u"已登出.")
    return redirect(url_for('home'))