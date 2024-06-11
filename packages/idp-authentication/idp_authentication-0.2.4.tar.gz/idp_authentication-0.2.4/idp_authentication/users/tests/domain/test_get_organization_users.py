def test_get_organization_users(container, user_2):
    get_organization_users_use_case = container.users_module().use_cases().get_organization_users()
    organization = user_2.user_roles[0].organization
    organization_users = get_organization_users_use_case.execute([organization])
    assert organization_users == [user_2]


def test_get_organization_users_with_role(container, user_4):
    get_organization_users_use_case = container.users_module().use_cases().get_organization_users()
    organization = user_4.user_roles[0].organization
    role = user_4.user_roles[0].role

    organization_users = get_organization_users_use_case.execute([organization], [role])
    assert organization_users == [user_4]
