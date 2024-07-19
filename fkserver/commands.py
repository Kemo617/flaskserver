from fkserver import app, db, click, User, Stock, SMTP, text

# ...

# ----------- list of commands ----------
# initdb
# setsmtp
# setuser
# activateuser
# decativateuser
# listusers
# liststocks
# listsmtp
# deleteuser
# deleteusertable
# deletestocktable


# 初始化数据库
@app.cli.command() 
# @click.option('--drop', is_flag=True, help='Create after drop.')
def initdb():
    db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

# 设置smtp信息
@app.cli.command()
@click.option('--server', prompt=True, help="The smtp server used to send emails.")
@click.option('--sendername', prompt=True, help="The sender's name.")
@click.option('--senderaddress', prompt=True, help="The sender's email account.")
@click.option('--password', prompt=True, help="The password used to send emails.")
def setsmtp(server, sendername, senderaddress, password):
    db.create_all()

    smtp = SMTP.query.first()
    if smtp is not None:
        click.echo('Updating smtp infos ...')
    else:
        click.echo('Creating smtp infos ...')
        smtp = SMTP()
        db.session.add(smtp)

    smtp.server = server
    smtp.sendername = sendername
    smtp.senderaddress = senderaddress
    smtp.password = password

    db.session.commit()
    click.echo('Done.')

# 创建用户
@app.cli.command()
@click.option('--username', prompt=True, help="The username used to login.")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="The password used to login.")
@click.option('--email', prompt=True, help="The user's email address.")
def setuser(username, password, email):
    db.create_all()

    user = User.query.filter_by(email=email).first()
    if user is not None:
        click.echo('Updating user ...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user ...')
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

# 激活用户
@app.cli.command()
@click.option('--username', prompt=True, help="Activate user.")
def activateuser(username):
    db.create_all()

    user = User.query.filter_by(username=username).first()
    if user is not None:
        if user.is_activated:
            click.echo('User %s already activated.' % username)
        else:
            click.echo('Activating user %s ...' % username)
            user.is_activated = True
            db.session.commit()
            click.echo('Done')
    else:
        click.echo('User not existed.')

# 设置用户为未激活
@app.cli.command()
@click.option('--username', prompt=True, help="Deactivate user.")
def deactivateuser(username):
    db.create_all()

    user = User.query.filter_by(username=username).first()
    if user is not None:
        if user.is_activated:
            click.echo('Deactivating user %s ...' % username)
            user.is_activated = False
            user.renewregistertime()
            db.session.commit()
            click.echo('Done')      
        else:
            user.renewregistertime()
            click.echo('User %s already deactivated.' % username)
    else:
        click.echo('User not existed.')

# 打印用户
@app.cli.command()
def listusers():
    db.create_all()

    for user in User.query.all():
        print('-- ', user.username, user.email)
        for stock in Stock.query.filter_by(username=user.username):
            print('  ', stock.stockname, end=' ')
        print('  ', user.random_send_id)

# 打印自选股票
@app.cli.command()
def liststocks():
    db.create_all()

    for stock in Stock.query.all():
        print(stock.username, ' ', stock.stockname)

# 打印smtp设置
@app.cli.command()
def listsmtp():
    db.create_all()

    smtp = SMTP.query.first()
    if smtp is not None:
        print('server:', smtp.server)
        print('sendername:', smtp.sendername)
        print('senderaddress:', smtp.senderaddress)
        print('password:', smtp.password)
  
# 删除用户
@app.cli.command()
@click.option('--username', prompt=True, help="Delete user.")
def deleteuser(username):
    db.create_all()

    user = User.query.filter_by(username=username).first()
    if user is not None:
        click.echo('Deleting user %s ...' % username)
        db.session.delete(user)
        # 删除对应的自选股
        click.echo('Deleting user stocks ...')
        for stock in Stock.query.filter_by(username=username):
            db.session.delete(stock)
        db.session.commit()
        click.echo('Done')
    else:
        click.echo('User not existed.')
        
# 删除用户表
@app.cli.command()
def deleteusertable():
    db.create_all()
    db.session.execute(text("DROP TABLE IF EXISTS users"))
    click.echo('Done')
    db.create_all()

# 删除股票表
@app.cli.command()
def deletestocktable():
    db.create_all()
    db.session.execute(text("DROP TABLE IF EXISTS stocks"))
    click.echo('Done')
    db.create_all()

# 删除股票基础信息表
@app.cli.command()
def deletestockbasetable():
    db.create_all()
    db.session.execute(text("DROP TABLE IF EXISTS stockbase"))
    click.echo('Done')
    db.create_all()

# 清理数据库
@app.cli.command()
def cleandb():
    db.create_all()
    # 清理删除用户后, 也许在个股表的残留, 待做
    click.echo('Done.')