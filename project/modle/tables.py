import pymongo
from modle import Field
import datetime
from modle.Field import Field as field
import uuid
from modle.db import mongodb
import json
from bson.objectid import ObjectId

conn = mongodb().db

class ModelMeta(type):
    def __new__(cls,class_name,parent_set,attrs_dict):
        # Model基类不做任何处理
        if class_name == "Model":
            return super(ModelMeta,cls).__new__(cls,class_name,parent_set,attrs_dict)
        # 将字段属性存放到__mapping__中
        fields = {k:v for k,v in attrs_dict.items() if isinstance(v,field)}
        fields["_id"]="UniqueStr"
        # for k in fields:
        #     attrs_dict.pop(k)
        #     pass
        attrs_dict["__mapping__"]=fields
        attrs_dict["__table__"]=class_name.lower()
        return super(ModelMeta,cls).__new__(cls,class_name,parent_set,attrs_dict)
        
class Model(dict,metaclass=ModelMeta):

    # _id = Field.IdField("_id")

    def __init__(self,_id=None,**kw):
        # setattr(self,"_id",_id)
        for k,v in kw.items():
            setattr(self,k,v)
    def __call__(self):
        return getattr(self,"_id")
    def __str__(self):
        return str(self.__dict__)

    def save(self):
        result = conn[self.__class__.__dict__["__table__"]].insert_one(self.__dict__)
        return result

    @classmethod 
    def get_exist(cls,kw):
        result = conn[cls.__dict__["__table__"]].find(kw)
        return result
    @classmethod 
    def get_one(cls,kw,show=None):
        
        '''
        author:Lixin
        date:20190416
        desc:根据传入条件获取符合的用户记录
        input:
        return:
        '''
       
        if show is None:
            result = conn[cls.__dict__["__table__"]].find_one(kw)
        else:
            more=dict()
            for field in show:
                more[field]=1
            result = conn[cls.__dict__["__table__"]].find_one(kw,more)    
        return result
    @classmethod
    def get_many(cls,kw,show=None):
        if show is None:
            result = conn[cls.__dict__["__table__"]].find(kw)
        else:
            more=dict()
            for field in show:
                more[field]=1
            result = conn[cls.__dict__["__table__"]].find(kw,more)    
        return result
    @classmethod
    def delete(cls,kw):
        result = conn[cls.__dict__["__table__"]].remove(kw)
        return result

    @classmethod
    def get_all(cls,show=None):
        if show is None:
            result = conn[cls.__dict__["__table__"]].find({})
        else:
            more=dict()
            for field in show:
                more[field]=1
            result=conn[cls.__dict__["__table__"]].find({},more)
        return result

    @classmethod
    def get_conn(cls):
        return conn[cls.__dict__["__table__"]]

class User(Model):
    name = Field.CharField("name")
    password = Field.CharField("password")
    email = Field.CharField("email")

class Friend(Model):
    user = Field.IdField("user")
    friend = Field.IdField("friend")

class ChatRoom(Model):
    '''
    room_name
    owner
    create_time
    '''
    room_name = Field.CharField("room_name")
    owner = Field.IdField("owner")
    create_time = Field.DataField("create_time")

class Members(Model):
    '''
    room
    member
    '''
    room = Field.IdField("room")
    member = Field.IdField("member")

class History(Model):
    room = Field.IdField("room")
    send_by = Field.IdField("send_by")
    send_time = Field.DataField("send_time")
    content = Field.CharField("content",MAX_LEN=400)