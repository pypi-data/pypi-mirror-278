import os
import re
from fastapi import APIRouter
import importlib
import inspect

METHODS = {
    'create': {
        'method': 'POST',
    },
    'find_all': {
        'method': 'GET',
    },
    'find_one': {
        'method': 'GET',
        'pk': True
    },
    'update_one': {
        'method': 'PATCH',
        'pk': True
    },
    'update_all': {
        'method': 'PUT',
        'pk': True
    },
    'remove': {
        'method': 'DELETE',
        'pk': True
    }
}


class DynamicRouter(APIRouter):
    def __init__(
        self,
        base: str = "apps",
        file: str = 'controller.py',
        *args,
        **kwargs,
    ):
        self._base = base
        self._file = file
        super().__init__(*args, **kwargs)
        self.build_router()

    def build_router(self):
        file_list = []
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), self.base)):
            for file in files:
                if re.match(f'{self._file}$', str(file)):
                    _file = os.path.join(root, file)
                    _file_router = re.sub('.py', '', str(_file))
                    file_list.append(os.path.join(root, file))
                    route_file = importlib.import_module(
                        os.path.relpath(root).replace(
                            "/", ".").replace('\\', '.') + "." + re.sub('.py', '', str(file))
                    )
                    find_routes = [r for r in dir(route_file) if r in METHODS.keys()]
                    if find_routes:
                        if os.path.basename(root) == self.base:
                            tags = ["default"]
                        else:
                            tags = [re.sub(
                                "[\/]controller$", "", str(os.path.relpath(_file_router, self.base)).replace("\\", "/"))]

                        # Replace \\ in window
                        uri = str(os.path.relpath(_file_router,
                                  self.base)).replace("\\", "/")
                        uri = re.sub("[\/]controller$", "", uri)
                        _router = APIRouter(
                            prefix="/" + uri,
                            tags=tags,
                        )

                        for r in find_routes:
                            func = getattr(route_file, r)
                            arg = self.get_first_arg(func)
                            suffix = '/' if len(arg) == 0 else '/{' + arg[0] +'}/'
                            _router.add_api_route(suffix, getattr(route_file, r), methods=[METHODS.get(r).get('method')])

                        self.include_router(_router)

    def convert_to_lower_with_hyphen(filename):
        lower_router = filename[0].lower()
        for char in filename[1:]:
            if char.isupper():
                lower_router += '-' + char.lower()
            else:
                lower_router += char

        return lower_router

    def get_first_arg(self, func):
        signature = inspect.signature(func)
        params = [param.name for param in signature.parameters.values()]
        return list(filter(lambda x: x not in ['kwargs'], params))
    
    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        self._base = value
