from idp_authentication.users.base_classes.base_repository import BaseRepository
from idp_authentication.users.domain.entities import UserRole
from idp_authentication.users.domain.ports.repository import UserRoleRepositoryPort


class UserRoleRepository(BaseRepository, UserRoleRepositoryPort):
    entity = UserRole

    def get_organization_names(self) -> list[str]:
        result = self.session.query(UserRole.organization).filter(UserRole.organization.is_not(None)).distinct().all()
        return [row[0] for row in result]
