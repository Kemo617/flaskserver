import os
import sys
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# ...

app = Flask(__name__)

login_manager = LoginManager(app)

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
# sqlite数据库路径
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 所需的会话密钥
app.config['SECRET_KEY'] = "Luffy is No.1!"

db = SQLAlchemy()
db.init_app(app)

# 放在最后, 整理引用关系, 避免循环引用
import smtplib
import click
import pytz
import json
from datetime import datetime
from uuid import uuid4
from sqlalchemy import text
from flask import url_for, render_template, session, request, flash, redirect, jsonify
from flask_login import login_required, login_user, logout_user, current_user, UserMixin
from flask_socketio import send, emit
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from werkzeug.security import generate_password_hash, check_password_hash
from email.message import EmailMessage
from datetime import datetime as dt
from fkserver import test
from fkserver.models.user import User
from fkserver.models.stockbase import Stockbase
from fkserver.models.stock import Stock
from fkserver.models.smtp import SMTP
from fkserver.controls.mail import send_confirm_mail, send_inform_mail
from fkserver.controls.common import get_users, getTimeNow, get_stockcodes, get_stockcodes_all, update_stockprices, get_send_id
from fkserver.controls.sendInformEmails import sendinformEmails
from fkserver.models.serverstatus import StockinfoSrcStatus, getStockinfoSrcStatusDesc
from fkserver.views import interface, home, login, register, refresh, errors
from fkserver.views.operations import add, delete, edit, update
import fkserver.commands

# 登录视图为起点
login_manager.login_view = 'login'
login_manager.login_message = ''

# 用户加载回调函数
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

# 模板上下文处理函数, 注入用户信息
@app.context_processor
def inject_user():
    return dict(user=current_user)

# 模板上下文处理函数, 注入股票信息
@app.context_processor
def inject_stocks():
    stocks = []
    
    try:
        stocks = Stock.query.filter_by(username=current_user.username).all()
    except BaseException as e:
        pass

    return dict(stocks=stocks)

# 模板上下文处理函数, 注入数据源状态
@app.context_processor
def inject_srcstatus():
    srcstatus = getStockinfoSrcStatusDesc()
    return dict(srcstatus=srcstatus)