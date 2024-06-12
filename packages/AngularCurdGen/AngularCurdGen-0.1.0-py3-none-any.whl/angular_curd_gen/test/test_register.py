from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel

from angular_curd_gen.register import ModelAdmin, generate_whole_app


class Users(BaseModel):
    id: int
    username: str
    password: Optional[str] = None
    firstname: str
    lastname: str
    nickname: str = ''
    gender: str
    birthday: date
    role: str
    email: str
    mobile: str
    address: str
    active: bool
    created: datetime


class Apps(BaseModel):
    id: int
    name: str
    appkey: str
    secret: str
    producer: str


class UsersAdmin(ModelAdmin):
    """用户管理注释文档信息"""
    model_readable_name = '用户'
    model_fields = ('id', 'username', 'lastname', 'firstname', 'gender', 'birthday', 'role', 'active', 'created')
    list_display_restraint = model_fields
    list_editable_restraint = ('username', 'gender')
    model_edit_fields = ('username', 'lastname', 'firstname', 'gender', 'birthday', 'active')
    model_create_fields = ('username', 'lastname', 'firstname', 'gender', 'birthday', 'role', 'active')
    model_translate_fields = ('ID', '用户名', '姓氏', '名字', '性别', '生日', '角色', '是否激活', '创建时间')


class AppsAdmin(ModelAdmin):
    """应用管理注释文档信息"""
    model_readable_name = '应用'
    model_fields = ('id', 'name', 'appkey', 'secret', 'producer')
    list_display_restraint = model_fields
    list_editable_restraint = ('name', 'producer')
    model_edit_fields = ('name', 'appkey', 'secret', 'producer')
    model_create_fields = model_edit_fields
    model_translate_fields = ('ID', '名称', 'AppKey', 'Secret', '生产者')


def test_register():
    generate_whole_app(model_admin=UsersAdmin, model=Users, app_name='first', app_readable_name='第一个应用')
    # generate_whole_app(model_admin=AppsAdmin, model=Apps, app_name='first', app_readable_name='纯应用')
