def test_get_organization_names(container):
    get_organization_names_user_case = container.users_module().use_cases().get_organization_names()
    organization_names = get_organization_names_user_case.execute()
    assert organization_names == ["Organization 1", "Organization 2"]
