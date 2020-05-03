import os, stat, uuid, json, re
import datetime

from flask import Blueprint, request, jsonify
from application import db, app
from werkzeug.utils import secure_filename


router_upload = Blueprint('upload_page', __name__)


@router_upload.route('/ueditor', methods=['GET', 'POST'])
def ueditor():
    # 加载ueditor  json 配置
    req = request.values
    action = req['action'] if 'action' in req else ''
    if action == 'config':
        root_path = app.root_path
        config_path = "{0}\\web\\static\\plugins\\ueditor\\upload_config.json".format(root_path)
        with open(config_path) as fp:
            try:
                conf_data = json.loads(re.sub(r'\/\*.*\*/', '', fp.read()))

            except Exception:
                conf_data = {}

    return jsonify(conf_data)

@router_upload.route('/pic', methods=['GET', 'POST'])
def uploadPic():

    resp = {
        'code': 200,
        'msg': '操作成功！',
        'data': {}
    }
    pic = request.files['pic']
    root_path = app.root_path + app.config['UPLOAD']['prefix_path']

    # 校验图片格式是否正确
    pic_ext = app.config['UPLOAD']['ext']
    # 获取文件后缀  .jpg ....
    ext = os.path.splitext(pic.filename)[1]
    if ext not in pic_ext:
        resp = {
            'code': -1,
            'msg': '该图片格式不符合要求！',
            'data': {}
        }
        print(resp)
        return jsonify(resp)

    file_dir = datetime.datetime.now().strftime('%Y%m%d')

    save_dir = root_path + '\\' + file_dir

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)
    pic_name = str(uuid.uuid4()).replace('_', '')+'.'+secure_filename(pic.filename)
    pic.save('{0}\\{1}'.format(save_dir, pic_name))

    return jsonify(resp)