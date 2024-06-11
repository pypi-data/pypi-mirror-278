from dataclasses import dataclass, field
from typing import Optional

from idp_authentication.custom_types import (
    AppEntitiesRestrictionsDict,
    PermissionRestrictionsDict,
)
from idp_authentication.users.base_classes.base_entity import BaseEntity


@dataclass(kw_only=True)
class UserRole(BaseEntity):
    role: str = field(default_factory=str)
    app_entities_restrictions: AppEntitiesRestrictionsDict | None = field(default=None)
    permission_restrictions: PermissionRestrictionsDict = field(default_factory=dict)
    user_id: Optional[str] = field(default=None)
    organization: Optional[str] = field(default=None)
