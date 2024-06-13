from idp_authentication.users.base_classes.base_use_case import UseCasePort
from idp_authentication.users.domain.ports.unit_of_work import UsersUnitOfWorkPort


class GetOrganizationNamesUseCase(UseCasePort):
    """
    Get all organization names from user roles.
    """

    def __init__(self, users_unit_of_work: UsersUnitOfWorkPort):
        self.users_unit_of_work = users_unit_of_work

    def execute(self) -> list[str]:
        with self.users_unit_of_work as uow:
            return uow.user_role_repository.get_organization_names()
