from tornado.web import RequestHandler,authenticated
from tornado.websocket import WebSocketHandler
from relylib import validimg
import config
from modle.db import mongodb
from modle.tables import User,ChatRoom,Members
from tornado.gen import coroutine
import random,time,hashlib,json,os

session=dict()
class ImgValidHandler(RequestHandler):
    def post(self,*args,**kwargs):
        remote_ip=self.request.remote_ip

        refersh = self.get_argument("refresh",None)
        if refersh is not None:
            img_num=session[remote_ip+"img_num"]

            if img_num != 0:
                os.remove(os.path.join(config.settings["static_path"],f"pic/valid{img_num}.png"))
            else:
                os.remove(os.path.join(config.settings["static_path"],f"pic/valid.png"))
            img_num=random.randint(1,10000)

            img,result=validimg.get_img()
            with open(os.path.join(config.settings["static_path"],f"pic/valid{img_num}.png"),"wb") as f:
                img.save(f,format="png")
            self.write(json.dumps({"path":f"/static/pic/valid{img_num}.png"}))

            session[remote_ip+"img_num"]=img_num
            session[remote_ip+"valid_num"]=result

class LoginHandler(RequestHandler):
    
    '''
    author:Lixin
    date:20190416
    desc:登录处理handler    
    input:
    return:登陆成功后跳转至聊天室页面，并记录登录状态
    '''
    def get(self,*args,**kwargs):
        remote_ip = self.request.remote_ip
        
        img,result=validimg.get_img()
        with open(os.path.join(config.settings["static_path"],f"pic/valid.png"),"wb") as f:
            img.save(f,format="png")

            session[remote_ip+"img_num"]=0
            session[remote_ip+"valid_num"]=result
        url = "/login?next="+self.get_argument("next",default="/main")
        self.render("login.html",title="登录",error="",name="",url=url)
        
    def post(self,*args,**kwargs):
        remote_ip = self.request.remote_ip
        validCheck = self.get_argument("ValidCheck",None)
         # 验证码检验    
        if validCheck is not None:
            valid = self.get_argument("val",None)
            if session[remote_ip+"valid_num"] != valid.upper():
                self.write(json.dumps({"wrong":True}))
            return

        name = self.get_argument("account",None)
        password = self.get_argument("password",None)


        result = User.get_one({"name":name,"password":password})

        if result is None:

            img_num = session[remote_ip+"img_num"]
            if img_num != 0:
                os.remove(os.path.join(config.settings["static_path"],f"pic/valid{img_num}.png"))
            else:
                os.remove(os.path.join(config.settings["static_path"],f"pic/valid.png"))

            img,result=validimg.get_img()
            with open(os.path.join(config.settings["static_path"],"pic/valid.png"),"wb") as f:
                img.save(f,format="png")

            session[remote_ip+"img_num"]=img_num
            session[remote_ip+"valid_num"]=result
            url = "/login?next="+self.get_argument("next",default="/main")
            self.render("login.html",title="登录",error="**用户名或密码错误，请重新输入**",name=name,url=url)
        else:
            m2 = hashlib.md5()
            m2.update(("logined"+str(random.randint(1,1000000))).encode())
            logined = m2.hexdigest()
            session[remote_ip+"logined"]=logined
            session[remote_ip+"user"]=result["_id"]
            self.redirect(self.get_argument("next",default="/main")+"?logined="+logined) 

class RegisterHandler(RequestHandler):
    
    '''
    author:Lixin
    date:20190416
    desc:注册处理Handler
    input:
    return:注册后返回登陆页面
    '''
    def get(self,*args,**kwargs):
        remote_ip=self.request.remote_ip
        # 注册时先清除该ip的验证码图片
        try:
            img_num=session[remote_ip+"img_num"]
            os.remove(os.path.join(config.settings["static_path"],f"pic/valid{img_num}.png"))
        except:
            pass

        img,result=validimg.get_img()
        with open(os.path.join(config.settings["static_path"],"pic/valid.png"),"wb") as f:
            img.save(f,format="png")
        
        session[remote_ip+"img_num"]=0
        session[remote_ip+"valid_num"]=result
        
        self.render("register.html",title="注册")

    def post(self,*args,**kwargs):
        remote_ip = self.request.remote_ip
        # 用户验证及邮箱验证
        Check = self.get_argument("Check",None)
        validCheck = self.get_argument("ValidCheck",None)
        if Check is not None:
            checkVal = self.get_argument("val",None)
            checkField = self.get_argument("field",None)
            result = User.get_one({checkField:checkVal})
            if result is not None:
                self.write(json.dumps({"exist":True}))
            return 
        # 验证码检验    
        if validCheck is not None:
            valid = self.get_argument("val",None)
            if session[remote_ip+"valid_num"] != valid.upper():
                self.write(json.dumps({"wrong":True}))
            return

        name = self.get_argument("account",None)
        password = self.get_argument("password",None)
        email = self.get_argument("email",None)
        user = User(name=name,password=password,email=email)
        result = user.save()
        time.sleep(2)
        self.redirect(self.reverse_url("login"))


class MainHandler(RequestHandler):
    
    
    '''
    author:Lixin
    date:20190416
    desc:聊天室主页面
    input:
    return:
    '''
    def get_current_user(self):
        remote_ip=self.request.remote_ip
        try:
            logined = session[remote_ip+"logined"]
            client_logined = self.get_argument("logined",default=None)
            return logined==client_logined
        except:
            self.send_error(900)
            return False
            
        
    def write_error(self,status_code,**kw):
        print(1)
        self.redirect(self.reverse_url("error"))
        print(2)

    @authenticated
    def get(self,*args,**kwargs):
        remote_ip=self.request.remote_ip
        user_id=session[remote_ip+"user"]
        # 获取本人所在群聊
        result = Members.get_many({"member":user_id})
        room_img=list()
        room_names=list()
        for member in result:
            room_img.append({ChatRoom.get_one({"_id":member["room"]})["room_name"]:"/static/pic/ulogo"+str(random.randint(1,11))+".jpg"})
            room_names.append(ChatRoom.get_one({"_id":member["room"]})["room_name"])
        
        # 获取未加入群聊
        all_room = ChatRoom.get_all()
        ni_room_list=list()
        ni_room_names = list()
        for room in all_room:
            ni_room_names.append(room["room_name"])
        # print(room_names)
        # print(ni_room_names)
        for room_name in room_names:
            if room_name in ni_room_names:
                ni_room_names.remove(room_name)
        for room_name in ni_room_names:
            ni_room_list.append({room_name:"/static/pic/ulogo"+str(random.randint(1,11))+".jpg"})
        self.render("mainpage.html",title="主页",rooms=room_img,ninrooms=ni_room_list)

class GroupHandler(RequestHandler):

    def post(self,*args,**kwargs):
        remote_ip = self.request.remote_ip
        user_id = session[remote_ip+"user"]
        action = self.get_argument("action",None)
        if action is not None:
            room_name = self.get_argument("val",None)
            
            if action=="join":
                room_id=ChatRoom.get_one({"room_name":room_name})["_id"]
                members = Members(room=room_id,member=user_id)
                members.save()
                self.write("1")
            elif (action=="quit"):
                room_id=ChatRoom.get_one({"room_name":room_name})["_id"]
                Members.delete({"member":user_id,"room":room_id})
                self.write("1")
            elif (action=="create"):
                result = ChatRoom.get_one({"room_name":room_name})
                if result is not None:
                    self.write("0")
                else:
                    chat_room = ChatRoom(room_name=room_name,owner=user_id)
                    result = chat_room.save()
                    room_id = result.inserted_id
                    member = Members(room=room_id,member=user_id)
                    member.save()
                    self.write("1")
            elif (action=="out"):
                del session[remote_ip+"user"]
                del session[remote_ip+"img_num"]
                del session[remote_ip+"valid_num"]
                del session[remote_ip+"logined"]
                self.write("1")
                # self.redirect(self.reverse_url("login"))

class WSChatHandler(WebSocketHandler):
    users=list()
    def open(self):
        remote_ip = self.request.remote_ip
        user_id=session[remote_ip+"user"]
        user_name = User.get_one({"_id":user_id})["name"]
        self.users.append(self)
    
    def on_message(self,message):
        remote_ip = self.request.remote_ip
        user_id=session[remote_ip+"user"]
        user_name = User.get_one({"_id":user_id})["name"]
        message = json.loads(message)
        room=message[0]
        msg=message[1]

        for user in self.users:
            if user.request.remote_ip!=remote_ip:
                print(user.request.remote_ip)
                user.write_message(json.dumps([room,user_name,msg]))


        # Members = tables.Members
        # members = Members.get_many({"room":room})
        # rooms = [members["member"] for _ in members if members["member"]!=user_id]
        # for room in rooms:
        #     message.append(user_name)
        #     self.write_message(json.dumps(message))
        # room=message[0]
        # msg=message[1]
        
        

    def on_close(self):
        remote_ip=self.request.remote_ip
        try:
            img_num=session[remote_ip+"img_num"]
            if img_num != 0:
                os.remove(os.path.join(config.settings["static_path"],f"pic/valid{img_num}.png"))
        except:
            pass

        # self.users.remove(self)
        # del session[remote_ip+"user"]
        # del session[remote_ip+"img_num"]
        # del session[remote_ip+"valid_num"]
        # del session[remote_ip+"logined"]

    def check_origin(self,origin):
        return True
class ErrorPageHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.render("error.html")