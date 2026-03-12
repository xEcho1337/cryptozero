import pkgutil
import importlib

from typing import Any, Dict
from cryptozero.attacks.base import CipherAttack

def scan_vulnerabilities(algorithm: str, params: Dict[str, Any]) -> Dict[str, bool]:
    results: Dict[str, bool] = {}
    module_path = f"cryptozero.attacks.{algorithm}"
    try:
        package = importlib.import_module(module_path)
    except ModuleNotFoundError:
        raise ValueError(f"Algorithm module '{algorithm}' not found")

    for finder, name, ispkg in pkgutil.iter_modules(package.__path__):
        if ispkg:
            continue
        full_name = f"{module_path}.{name}"
        mod = importlib.import_module(full_name)

        for attr in dir(mod):
            cls = getattr(mod, attr)
            try:
                if isinstance(cls, type) and issubclass(cls, CipherAttack) and cls is not CipherAttack:
                    attack: CipherAttack = cls(**params)
                    try:
                        vuln = attack.is_vulnerable()
                    except Exception:
                        vuln = False
                    results[attr] = vuln
            except TypeError:
                continue
    return results
