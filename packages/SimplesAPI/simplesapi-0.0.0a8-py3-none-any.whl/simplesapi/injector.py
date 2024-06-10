from fastapi import Depends, Path
from typing import Callable, Any
import inspect

def inject_dependencies_and_params(handler: Callable[..., Any]) -> Callable[..., Any]:
    async def wrapper(*args, **kwargs):
        # Inspecionar a assinatura da função handler para determinar os parâmetros necessários
        signature = inspect.signature(handler)
        params = signature.parameters

        # Criar um dicionário de parâmetros para serem injetados
        injected_params = {}
        for param_name, param in params.items():
            if param.annotation is not inspect.Parameter.empty:
                if param.annotation is Path:
                    injected_params[param_name] = Path()
                else:
                    injected_params[param_name] = Depends(param.annotation)

        # Chamar a função handler com os parâmetros injetados
        return await handler(*args, **injected_params)
    return wrapper
