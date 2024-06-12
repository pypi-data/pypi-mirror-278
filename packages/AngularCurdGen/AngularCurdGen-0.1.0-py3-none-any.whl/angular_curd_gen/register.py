from dataclasses import dataclass
from pathlib import Path

import inflect
from jinja2 import FileSystemLoader, Environment
from parse import parse
from pydantic import BaseModel

from angular_curd_gen.admin import ModelAdmin
from angular_curd_gen.config import TEMPLATE_DIR, BACKEND_TEMPLATE_DIR, FRONTEND_TEMPLATE_DIR


@dataclass
class ModelRegister:
    """"""
    model_admin: ModelAdmin = None
    model: BaseModel = None

    app_name: str = ''  # app name run in code
    app_readable_name: str = ''  # show in page
    app_title_name = ''

    # extract model info
    model_name = ''  # is single
    models_name = ''  # is plural
    lower_model_name = ''
    lower_models_name = ''
    model_fields_map = None  # all model fields with type dict[str,type]
    jinja_env = None
    output_angular_dir = ''

    # extract model admin info
    model_admin_fields = ()

    def register(self):
        """run all"""
        self._prepare()
        gen_functions = [i for i in dir(self) if i.startswith('gen_')]
        for f in gen_functions:
            getattr(self, f)()

    def _prepare(self):
        # model
        engine = inflect.engine()

        self.app_title_name = self.app_name.title()

        self.model_name = engine.singular_noun(self.model.__name__) or self.model.__name__
        self.models_name = engine.plural(self.model_name)

        self.lower_model_name = self.model_name.lower()
        self.lower_models_name = self.models_name.lower()

        self.model_fields_map = self.model.__dict__['__annotations__']

        # model admin
        self.model_admin_fields = tuple([i for i in dir(self.model_admin) if not i.startswith('_')])
        if not self.model_admin.model_translate_fields:
            self.model_admin.model_translate_fields = self.model_admin.model_fields

        # template
        loader = FileSystemLoader(TEMPLATE_DIR)
        self.jinja_env = Environment(loader=loader)

        self.out_app_dir = Path(f"{self.app_name}")

        self.out_rust_dir = self.out_app_dir / BACKEND_TEMPLATE_DIR
        self.output_angular_dir = self.out_app_dir / FRONTEND_TEMPLATE_DIR
        self.out_rust_src_dir = self.out_rust_dir / 'src'

        self.output_angular_dir.mkdir(parents=True, exist_ok=True)
        self.out_rust_src_dir.mkdir(parents=True, exist_ok=True)
        (self.output_angular_dir / self.lower_model_name).mkdir(parents=True, exist_ok=True)

    def _load_template(self, name: str):
        return self.jinja_env.get_template(name)

    def _draw_template(self, template_name: str, target: str, project: str = 'angular'):
        """
        :param template_name:
        :param target:
        :param project: angular/rust
        :return:
        """
        template = self._load_template(template_name)
        context = self._build_context()
        rendered_content = template.render(context)
        match project:
            case 'angular':
                output_file = self.output_angular_dir / target
            case 'rust':
                output_file = self.out_rust_dir / target
            case _:
                raise ValueError(f"not support project {project}")

        with output_file.open('w', encoding='utf8') as file:
            file.write(rendered_content)

    def _draw_component(self, component_name: str, level: str = 'model'):
        templates = ['ts', 'css', 'html', 'spec.ts']
        for template in templates:
            template_name = f'{component_name}_component/{template}.jinja'
            match level:
                case 'model':
                    target_prefix = f"{self.lower_model_name}-{component_name}"
                    father_dir = self.output_angular_dir / self.lower_model_name / target_prefix
                    target_dir = f"{self.lower_model_name}/{target_prefix}"
                case 'app':
                    target_prefix = f"{self.app_name}-{component_name}"
                    father_dir = self.output_angular_dir / target_prefix
                    target_dir = f"{target_prefix}"
                case _:
                    raise ValueError(f"not support level {level}")
            father_dir.mkdir(parents=True, exist_ok=True)
            target = f"{target_dir}/{target_prefix}.component.{template}"
            self._draw_template(template_name=template_name, target=target, project='angular')

    @staticmethod
    def extract_py_type(t):
        type_str = parse("<class '{type}'>", str(t))
        if not type_str:  # option
            type_str = parse("typing.Optional[{type}]", str(t))

        the_type = type_str.named['type']
        return the_type

    def map_ts_type(self, t):
        the_type = self.extract_py_type(t)

        match the_type:
            case 'int' | 'float':
                return 'number'
            case 'str':
                return 'string'
            case 'bool':
                return 'boolean'
            case 'datetime.datetime' | 'datetime.date':
                return 'Date'
            case _:
                raise ValueError(f"not support type {t}")

    def map_rust_type(self, t):
        the_type = self.extract_py_type(t)

        match the_type:
            case 'int':
                return 'i64'
            case 'float':
                return 'f64'
            case 'str':
                return 'String'
            case 'bool':
                return 'bool'
            case 'datetime.datetime':
                return 'DateTime'
            case 'datetime.date':
                return 'NaiveDate'
            case _:
                raise ValueError(f"not support type {t}")

    def _build_context(self) -> dict:
        base_context = {
            'app_name': self.app_name,
            'app_readable_name': self.app_readable_name,
            'app_title_name': self.app_title_name,
            'model_name': self.model_name,
            'models_name': self.models_name,
            'lower_models_name': self.lower_models_name,
            'lower_model_name': self.lower_model_name,
            'fields_map': self.model_fields_map,
            'fields_translate_map': dict(zip(self.model_admin.model_fields, self.model_admin.model_translate_fields)),
            'cls': self
        }
        model_admin_context = {}
        for k in self.model_admin_fields:
            k_value = getattr(self.model_admin, k)
            model_admin_context[k] = k_value

            if k.endswith('_fields'):
                model_admin_context[f"{k}_type_map"] = {k1: v1 for k1, v1 in self.model_fields_map.items() if
                                                        k1 in k_value}
            if k.endswith('_restraint'):
                model_admin_context[f"{k}_translate"] = [base_context['fields_translate_map'][v] for v in k_value]
                model_admin_context[f"{k}_type_map"] = {v: self.model_fields_map[v]
                                                        for v in k_value}

        context = base_context | model_admin_context
        return context


@dataclass
class AngularModelRegister(ModelRegister):
    """"""

    def gen_a_interface(self):
        template = 'interfaces.jinja'
        target = f"{self.model_name}/{self.lower_model_name}_interfaces.ts"
        self._draw_template(template_name=template, target=target, project='angular')

    def gen_b_api(self):
        template = 'api.jinja'
        target = f"{self.model_name}/{self.lower_model_name}_api.service.ts"
        self._draw_template(template_name=template, target=target, project='angular')

    def gen_b1_api_spec(self):
        template = 'api.spec.jinja'
        target = f"{self.model_name}/{self.lower_model_name}_api.service.spec.ts"
        self._draw_template(template_name=template, target=target, project='angular')

    def gen_c_module(self):
        template = 'module.jinja'
        target = f"{self.app_name}.module.ts"
        self._draw_template(template_name=template, target=target, project='angular')

    def gen_d_router(self):
        template = 'routers.jinja'
        target = f"{self.app_name}-routing.module.ts"
        self._draw_template(template_name=template, target=target, project='angular')

    def gen_e_app_components(self):
        components = ['dashboard']
        for component in components:
            self._draw_component(component_name=component, level='app')

    def gen_e_model_components(self):
        components = ['list', 'creator', 'updater']
        for component in components:
            self._draw_component(component_name=component, level='model')


@dataclass
class RustModelRegister(ModelRegister):
    """"""

    def gen_f_rust_project_files(self):
        """Generate rust project with rust"""
        rust_template_dir = Path(TEMPLATE_DIR) / BACKEND_TEMPLATE_DIR
        for file in rust_template_dir.iterdir():
            if file.is_file() and file.name.endswith('.jinja'):
                template_name = file.name.removesuffix('.jinja')
                self._draw_template(
                    template_name=f"{BACKEND_TEMPLATE_DIR}/{file.name}",
                    target=template_name, project=BACKEND_TEMPLATE_DIR)

    def gen_g_rust_scripts(self):
        template_dir = Path(TEMPLATE_DIR) / BACKEND_TEMPLATE_DIR / 'src'
        for file in template_dir.iterdir():
            if file.is_file() and file.name.endswith('.jinja'):
                template_name = file.name.removesuffix('.jinja')
                self._draw_template(
                    template_name=f"{BACKEND_TEMPLATE_DIR}/src/{file.name}",
                    target=f"src/{template_name}", project=BACKEND_TEMPLATE_DIR)

    def gen_h_rust_sub_modules(self):
        """Generate rust sub modules"""
        template_dir = Path(TEMPLATE_DIR) / BACKEND_TEMPLATE_DIR / 'src'

        for folder in template_dir.iterdir():
            if folder.is_dir():
                (self.out_rust_src_dir / folder.name).mkdir(parents=True, exist_ok=True)
                for file in folder.iterdir():
                    if file.is_file() and file.name.endswith('.jinja'):
                        template_name = file.name.removesuffix('.jinja')
                        target = f"src/{folder.name}/{template_name}".replace('model', self.lower_model_name)
                        self._draw_template(
                            template_name=f"{BACKEND_TEMPLATE_DIR}/src/{folder.name}/{file.name}",
                            target=target, project=BACKEND_TEMPLATE_DIR)


def generate_whole_app(app_name: str, app_readable_name: str, model: BaseModel, model_admin: ModelAdmin):
    """generate whole app"""
    amr = AngularModelRegister(model_admin=model_admin, model=model, app_name=app_name,
                               app_readable_name=app_readable_name)
    amr.register()
    rmr = RustModelRegister(model_admin=model_admin, model=model, app_name=app_name,
                            app_readable_name=app_readable_name)
    rmr.register()
