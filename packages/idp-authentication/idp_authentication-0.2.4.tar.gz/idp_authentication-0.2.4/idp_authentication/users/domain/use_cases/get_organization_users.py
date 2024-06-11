from typing import Iterable

from idp_authentication import User
from idp_authentication.users.base_classes.base_use_case import UseCasePort
from idp_authentication.users.domain.ports.unit_of_work import UsersUnitOfWorkPort


class GetOrganizationUsersUseCase(UseCasePort):
    """
    Get all the users of the organization.
    """

    def __init__(self, users_unit_of_work: UsersUnitOfWorkPort):
        self.users_unit_of_work = users_unit_of_work

    def execute(self, organization_names: list[str], roles: list[str] = None) -> Iterable[User]:
        with self.users_unit_of_work as uow:
            return uow.user_repository.get_organization_users(organization_names, roles)
