from typing import Any, Optional, TypedDict, TypeVar, Union

T = TypeVar("T")
Role = str
ALL = "all"

AppEntityType = str
AppEntityIdentifier = Any
PermissionIdentifier = str

# AppEntitiesRestrictionsDict = {<entity_type>: [1, 2]}
AppEntitiesRestrictionsDict = dict[AppEntityType, list[AppEntityIdentifier]]

# PermissionRestrictionsDict = {"perform_operation_1": {<entity_type>: [1, 2]}, "perform_operation_2": false}
PermissionRestrictionsDict = dict[
    PermissionIdentifier, dict[AppEntityType, list[AppEntityIdentifier] | bool]
]


class AppSpecificConfigs(TypedDict):
    app_entities_restrictions: Optional[dict[str, list]]
    permission_restrictions: dict[str, Union[bool, Any]]
    organization: Optional[str]


UserAppSpecificConfigs = dict[Role, AppSpecificConfigs]


class UserTenantData(TypedDict):
    first_name: str
    last_name: str
    username: str
    email: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    date_joined: str
    app_specific_configs: UserAppSpecificConfigs
    is_demo: bool


class AppEntityEventMessage(TypedDict):
    app_identifier: str
    app_entity_type: str
    label: str
    record_identifier: Any
    tenant: Optional[str]
    deleted: bool


AppIdentifier = str
TenantIdentifier = str


UserRecordAppSpecificConfigs = dict[
    AppIdentifier, dict[TenantIdentifier, AppSpecificConfigs]
]


class UserRecordDict(TypedDict):
    first_name: str
    last_name: str
    username: str
    email: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    date_joined: str
    app_specific_configs: UserRecordAppSpecificConfigs
    is_demo: bool


class AppEntityRecordEventDict(TypedDict):
    app_identifier: str
    app_entity_type: str
    record_identifier: Any
    deleted: bool
    label: Optional[str]
