## Install

## Usage
- generate angular codes
```python
# declare model by pydantic
class Users(BaseModel):
    id: int
    username: str
    password: Optional[str] = None
    firstname: str
    lastname: str
    nickname: str = ''
    gender: str
    birthday: str
    role: str
    email: str
    mobile: str
    address: str
    active: int
    created: datetime

# declare model admin
class UsersAdmin(ModelAdmin):
    model_fields = ('id', 'username', 'lastname', 'firstname', 'gender', 'birthday', 'role', 'active', 'created')
    list_display_restraint = model_fields
    list_editable_restraint = ('username', 'gender')
    model_edit_fields = ('username', 'lastname', 'firstname', 'gender', 'birthday', 'role', 'active')
    model_create_fields = model_edit_fields
    model_translate_fields = ('ID', '用户名', '姓氏', '名字', '性别', '生日', '角色', '是否激活', '创建时间')

# generate angular codes
mr = ModelRegister(model_admin=UsersAdmin, model=Users, app_name='first')
mr.register()

# copy all files to angular src/app
```
- add module to imports in app.module.ts or add module router to imports in app-routing.module.ts

### frontend
#### once
- install
```bash
ng new project-name --no-standalone
ng add ng-zorro-antd
npm install dayjs
```
#### code
- env
```bash
ng g environments # angular17
# set backend: 'http://localhost:8000'

```
- config icon
- angular.json
```
"styles": [
  "node_modules/ng-zorro-antd/ng-zorro-antd.min.css",
  "src/styles.css"
],
```
- app.component.html
```html
<router-outlet></router-outlet>
```
#### module
1. add module to imports in app.module.ts
2. or add module router to imports in app-routing.module.ts





