from flask import Blueprint,request
from application import app
from common.models.good.Goods import Good,db
from common.libs.Helper import ops_render,getCurrentDate,iPagination
from sqlalchemy import or_
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager

router_goods = Blueprint("goods_page",__name__)

@router_goods.route('/index')
def index():
    resp_data={}
    list=Good.query.all()
    resp_data['list']=list

    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Good.query

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Good.status == int(req['status']))
    if 'mix_kw' in req:
        rule = or_( Good.name.ilike("%{0}%".format(req['mix_kw'])),Good.mobile.ilike("%{0}%".format(req['mix_kw'])) )
        query = query.filter(rule)

    params = {
        'total':query.count(),
        'page':page,
        'page_size':app.config['PAGE_SIZE'],
        'url':request.full_path.replace("&p={}".format(page),"")
    }
    # 分页的三大关键字
    pages = iPagination(params)
    offset = (page-1)*app.config['PAGE_SIZE']
    limit = page*app.config['PAGE_SIZE']

    list = query.all()[offset:limit]
    resp_data['list'] = list 
    resp_data['status'] = {
        "1":"正常",
        "0":"已删除"
    }
    resp_data['pages'] = pages

    return ops_render('/goods/index.html',resp_data)

@router_goods.route( "/info" )
def info():

    resp_data = {}
    req = request.values
    uid = int(req.get("id",0))
    info = Good.query.filter_by(id=uid).first()

    resp_data['info'] = info

    return ops_render('goods/info.html',resp_data)



@router_goods.route( "/set" ,methods = [ 'GET','POST'] )
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int(req.get("id",0))
        info = None
        if uid:
            info = Good.query.filter_by(id=uid).first()
        resp_data['info'] = info
        return ops_render('goods/set.html',resp_data)
    # POST  更新数据库

    resp = {
        'code':200,
        'msg':"操作成功",
        'data':{}
    }

    # ajax 发送的数据
    req = request.values
    id = req['id'] if 'id' in req else 0
    name = req['name'] if 'name' in req else ''
    price = req['price'] if 'price' in req else ''
    summary= req['summary'] if 'summary' in req else ''
    stock = req['stock'] if 'stock' in req else ''
    tags = req['tags'] if 'tags' in req else ''

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的昵称"
        return jsonify(resp)

    if price is None or len(price) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的昵称"
        return jsonify(resp)

    if summary is None or len(summary) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的昵称"
        return jsonify(resp)

    if stock is None or len(stock) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的库存"
        return jsonify(resp)
    
    user_info = Good.query.filter_by(id = id).first()
    if user_info:
        model_user = user_info
    else:
        model_user = Good()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.generateSalt()

    model_user.name = name
    

    # if user_info and user_info.uid == 1:
    #     resp['code'] = -1
    #     resp['msg'] = "该用户为Bruce，不允许修改"
    #     return jsonify(resp)
    # model_user.login_pwd = UserService.generatePwd(login_pwd,model_user.login_salt)
    model_user.updated_time = getCurrentDate()
    
    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)

@router_goods.route( "/cat" )
def cat():
    resp_data = {}
    return ops_render( "goods/cat.html",resp_data )

@router_goods.route( "/cat-set",methods = [ "GET","POST" ] )
def catSet():
    resp_data = {}
    return ops_render( "goods/cat_set.html",resp_data )