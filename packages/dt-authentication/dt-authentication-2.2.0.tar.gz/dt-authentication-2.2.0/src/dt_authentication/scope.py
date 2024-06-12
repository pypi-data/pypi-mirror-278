import dataclasses
import json
from typing import Dict, Union, Optional, List


@dataclasses.dataclass
class Scope:
    action: str
    resource: Optional[str] = None
    identifier: Optional[str] = None
    service: Optional[str] = None

    def __post_init__(self):
        self._sanity_check()

    def _sanity_check(self):
        if self.action is None:
            raise ValueError("Field 'action' cannot be none")
        if self.identifier is not None and self.resource is None:
            raise ValueError("If you set the field 'identifier' you must also set the field 'resource'")

    def grants(self, action: str, resource: Optional[str] = None, identifier: Optional[str] = None,
               service: Optional[str] = None) -> bool:
        if action != self.action:
            return False
        if self.resource is not None and self.resource != resource:
            return False
        if self.identifier is not None and self.identifier != identifier:
            return False
        if self.service is not None and self.service != service:
            return False
        return True

    @classmethod
    def parse(cls, scope: Union[str, Dict[str, str]]) -> 'Scope':
        if isinstance(scope, str):
            if scope.startswith("{"):
                return Scope(**json.loads(scope))
            scope_parts = scope.split(":")
            if len(scope_parts) > 3:
                raise ValueError("Only scopes in the form '<action>[:<resource>[:<resource-id>]]' "
                                 "are supported.")
            return Scope(*scope_parts)
        if isinstance(scope, dict):
            return Scope(**scope)
        else:
            raise ValueError(f"Scope of type '{type(scope).__name__}' not supported. "
                             f"Expected 'str' or 'dict'.")

    def compact(self, exclude: List[str] = None, force_dict: bool = False) -> Union[str, dict]:
        self._sanity_check()
        # resource is optional
        extras: List[str] = [self.resource] if self.resource is not None else []
        # make sure the exclusion list is valid
        exclude: List[str] = exclude or []
        choices: List[str] = ["identifier", "service"]
        for e in exclude:
            if e not in choices:
                raise ValueError(f"Field to exclude '{e}' not recognized. Valid choices are {str(choices)}.")
        extras += ([self.identifier] if "identifier" not in exclude else [])
        # without 'service' we use the string form
        if (not force_dict) and (self.service is None or "service" in exclude):
            return ":".join(filter(lambda x: x is not None, [self.action] + extras))
        # dict form instead
        return dataclasses.asdict(self)

    def __str__(self):
        return json.dumps(self.compact(), sort_keys=True) if self.service is not None else self.compact()
