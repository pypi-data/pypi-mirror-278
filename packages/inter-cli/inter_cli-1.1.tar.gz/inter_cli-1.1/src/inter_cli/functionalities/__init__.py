from src.inter_cli.functionalities.factory import (
    import_modules,
    factory,
    register_functionality,
)

__all__ = [
    "factory",
    "register_functionality",
]

import_modules("v1")
