import numbers
from datetime import datetime
import uuid
from bson.objectid import ObjectId

class Field():
    def __init__(self,column_name=None):
        if column_name is None:
            raise ValueError("Field need column_name")
        self.column_name = column_name

class CharField(Field):
    def __init__(self,column_name,MAX_LEN=50):
        if MAX_LEN is None:
            raise ValueError(f"{self.column_name} must spicify the max_len")
        elif not isinstance(MAX_LEN,int):
            raise ValueError(f"{self.column_name} max_len expect 'int' type")
        elif MAX_LEN<0:
            raise ValueError(f"{self.column_name} expect a positive number")
        self.max_len=MAX_LEN
        super(CharField,self).__init__(column_name)

    def __get__(self,instance,owner):
        return instance.__dict__[self.column_name]
    def __set__(self,instance,value):
        if isinstance(value,str):
            if (len(value)>self.max_len):
                raise ValueError(f"{self.column_name} out of MAX_LEN")
            else:
                instance.__dict__[self.column_name]=value
        else:
            raise ValueError(f"{self.column_name} type 'str' expected")

class IntField(Field):
    def __init__(self,column_name,MIN=None,MAX=None):
        if MIN is None:
            raise ValueError(f"{self.column_name} must spicify a min value")
        elif not isinstance(MIN,numbers.Integral):
            raise ValueError(f"{self.column_name} type 'int' expected")
        if MAX is None:
            raise ValueError(f"{self.column_name} must spicify a max value")
        elif not isinstance(MAX,numbers.Integral):
            raise ValueError(f"{self.column_name} type 'int' expected")
        if MIN>MAX:
            raise ValueError(f"{self.column_name} MIN larger than MAX")
        self.min=MIN
        self.max=MAX
        super(IntField,self).__init__(column_name)

    def __get__(self,instance,owner):
        return instance.__dict__[self.column_name]
    def __set__(self,instance,value,*args,**kw):
        if not isinstance(value,int):
            raise ValueError(f"{self.column_name} type 'int' expected")
        elif value>self.max or value <self.min:
            raise ValueError(f"{self.column_name} value between MIN and MAX needed")
        instance.__dict__[self.column_name]=value

class DataField(Field):
    def __init__(self,column_name,AUTO_NOW=True):
        self.auto_now=AUTO_NOW
        if AUTO_NOW:
            self.vauto_alue = datetime.now()
        super(DataField,self).__init__(column_name)        

    def __get__(self,instance,owner):
        return instance.__dict__[self.column_name]
    def __set__(self,instance,value):
        if self.auto_now:
            instance.__dict__[self.column_name]=self.vauto_alue
        if not isinstance(value,datetime):
            raise ValueError(f"{self.column_name} type 'datetime' expected")
        else:
            instance.__dict__[self.column_name]=value

class IdField(Field):
    def __init__(self,column_name):
        super(IdField,self).__init__(column_name)        

    def __get__(self,instance,owner):
        return instance.__dict__[self.column_name]

    def __set__(self,instance,value):
        if not isinstance(value,ObjectId):
            raise ValueError(f"{self.column_name} type 'ObjectId' expected")
        else:
            instance.__dict__[self.column_name]=value