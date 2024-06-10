
import importlib
import os
from simplesapi.internal_logger import simplesapi_internal_logger


logger = simplesapi_internal_logger()


def _import_handler(module_path, handler_name="handler"):
    spec = importlib.util.spec_from_file_location("routes", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, handler_name)

def _create_route_from_file(app, file_path: str, base_path: str) -> None:
    parts = file_path.split(os.sep)
    method_file_result = parts[-1].split('.')[0].split('__')
    
    last_route = method_file_result[0] if len(method_file_result) > 1 else None
    last_route = last_route.replace('[', '{').replace(']', '}')
    method = method_file_result[-1].upper()
    
    route = os.sep.join(parts[:-1])
    route = route.replace(base_path, '', 1)
    route = route.replace('[', '{').replace(']', '}')
    route = '/' + route.strip(os.sep).replace(os.sep, "/") + "/" if len(route) > 0 else "/"
    
    if last_route:
        route += last_route

    # TODO: remove if keep unused
    route_params = _extract_route_params(route)

    handler = _import_handler(file_path)

    available_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    if method in available_methods:
        app.add_api_route(route, handler, methods=[method.upper()])    
        logger.info(f"Added route {method.upper()} {route}")

def _extract_route_params(route: str):
    route_params = {}
    route_parts = route.split('/')
    for part in route_parts:
        if part.startswith('{') and part.endswith('}'):
            param_name = part[1:-1]
            route_params[param_name] = None

def register_routes(app, base_path:str):
    base_path = base_path.replace("/", os.sep)
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                _create_route_from_file(app, file_path, base_path)
