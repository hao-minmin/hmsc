from flask import Blueprint,render_template
# 引入蓝图路由

router_user=Blueprint('user_page',__name__)

# 给当前的app注册一个 user_page开头的路由

# 登录的路由
@router_user.route("/login")
def login():
    return render_template('user/login.html')

# 登录的路由
@router_user.route("/loginout")
def loginout():
    return "登出"

# 登录的路由
@router_user.route("/edit")
def edit():
    return "编辑"

# 登录的路由
@router_user.route("/reset-pwd")
def resetPwd():
    return "重置密码"