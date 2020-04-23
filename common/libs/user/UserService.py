import base64
import hashlib 
class UserService():
    # 结合salt  和 md5  生成新的密码
    @staticmethod
    def generatePwd(pwd,salt):
        m = hashlib.md5()
        str="%s-%s"%(base64.encodebytes(pwd.encode('utf-8')),salt)
        m.update(str.encode("utf-8"))
        # 新密码
        return m.hexdigest()
    # 对cookie 中存储的信息加密
    @staticmethod
    def generateAuthCode(user_info=None):
        m = hashlib.md5()
        str ="%s-%s-%s-%s"%(user_info.uid,user_info.login_name,user_info.login_pwd,user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()