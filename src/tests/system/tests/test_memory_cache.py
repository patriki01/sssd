import pytest

from lib.sssd.roles.client import Client
from lib.sssd.roles.generic import GenericProvider
from lib.sssd.topology import KnownTopologyGroup


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__getpwnam(client: Client, provider: GenericProvider):
    """
    :title: User is able to id(name) after SSSD is stopped
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that results have correct names
        3. Stop SSSD
        4. Find 'user1', 'user2' and 'user3' with id(name)
        5. Check that results have correct names
    :expectedresults:
        1. Users are found
        2. Users have correct names
        3. SSSD is stopped
        4. Users are found
        5. Users have correct names
    :customerscenario: False
    """
    provider.user('user1').add()
    provider.user('user2').add()
    provider.user('user3').add()

    client.sssd.start()

    for i in range(2):
        for user in ['user1', 'user2', 'user3']:
            result = client.tools.id(user)
            assert result is not None
            assert result.user.name == user
        if i == 0:
            client.sssd.stop()


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__getgrnam(client: Client, provider: GenericProvider):
    """
    :title: Group is able to getent.group(name) after SSSD is stopped
    :setup:
        1. Add 'group1', 'group2' and 'group3' to SSSD
        2. Start SSSD
    :steps:
        1. Find 'group1', 'group2' and 'group3' with getent.group(name)
        2. Check that groups have correct names
        3. Stop SSSD
        4. Find 'group1', 'group2' and 'group3' with getent.group(name)
        5. Check that groups have correct names
    :expectedresults:
        1. Groups are found
        2. Groups have correct names
        3. SSSD is stopped
        4. Groups are found
        5. Groups have correct names
    :customerscenario: False
    """
    provider.group('group1').add()
    provider.group('group2').add()
    provider.group('group3').add()

    client.sssd.start()

    for i in range(2):
        for group in ['group1', 'group2', 'group3']:
            result = client.tools.getent.group(group)
            assert result is not None
            assert result.name == group
        if i == 0:
            client.sssd.stop()


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__disabled_passwd_getgrnam(client: Client, provider: GenericProvider):
    """
    :title: Group is able to getent.group(name) after 'memcache_size_passwd' is set to '0' and SSSD is stopped
    :setup:
        1. Add 'group1', 'group2' and 'group3' to SSSD
        2. In SSSD nss change 'memcache_size_passwd' to '0'
        3. Start SSSD
    :steps:
        1. Find 'group1', 'group2' and 'group3' with getent.group(name)
        2. Check that groups have correct names
        3. Stop SSSD
        4. Find 'group1', 'group2' and 'group3' with getent.group(name)
        5. Check that groups have correct names
    :expectedresults:
        1. Groups are found
        2. Groups have correct names
        3. SSSD is stopped
        4. Groups are found
        5. Groups have correct names
    :customerscenario: False
    """
    provider.group('group1').add()
    provider.group('group2').add()
    provider.group('group3').add()

    client.sssd.nss['memcache_size_passwd'] = '0'
    client.sssd.start()

    for i in range(2):
        for group in ['group1', 'group2', 'group3']:
            result = client.tools.getent.group(group)
            assert result is not None
            assert result.name == group
        if i == 0:
            client.sssd.stop()


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__disabled_passwd_getpwnam(client: Client, provider: GenericProvider):
    """
    :title: User is not able to id(name) after 'memcache_size_passwd' is set to '0' and SSSD is stopped
    :setup:
        1. Add users to SSSD
        2. Set users uids
        3. In SSSD nss change 'memcache_size_passwd' to '0'
        4. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that users have correct names
        3. Stop SSSD
        4. Find users with id(name)
        5. Find users with id(uid)
    :expectedresults:
        1. Users are found
        2. Users have correct names
        3. SSSD is stopped
        4. Users are not found
        5. Users are not found
    :customerscenario: False
    """
    provider.user('user1').add(uid=10001)
    provider.user('user2').add(uid=10002)
    provider.user('user3').add(uid=10003)

    client.sssd.nss['memcache_size_passwd'] = '0'
    client.sssd.start()

    for user in ['user1', 'user2', 'user3']:
        result = client.tools.id(user)
        assert result is not None
        assert result.user.name == user

    client.sssd.stop()

    for user in ['user1', 'user2', 'user3', 10001, 10002, 10003]:
        assert client.tools.id(user) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__disabled_intitgroups_getgrnam(client: Client, provider: GenericProvider):
    """
    :title: Group is able to getent.group(name) after 'memcache_size_initgroups' is set to '0' and SSSD is stopped
    :setup:
        1. Add 'group1', 'group2' and 'group3' to SSSD
        2. In SSSD nss change 'memcache_size_initgroups' to '0'
        3. Start SSSD
    :steps:
        1. Find 'group1', 'group2' and 'group3' with getent.group(name)
        2. Check that groups have correct names
        3. Stop SSSD
        4. Find 'group1', 'group2' and 'group3' with getent.group(name)
        5. Check that groups have correct names
    :expectedresults:
        1. Groups are found
        2. Groups have correct names
        3. SSSD is stopped
        4. Groups are found
        5. Groups have correct names
    :customerscenario: False
    """
    provider.group('group1').add()
    provider.group('group2').add()
    provider.group('group3').add()

    client.sssd.nss['memcache_size_initgroups'] = '0'
    client.sssd.start()

    for i in range(2):
        for group in ['group1', 'group2', 'group3']:
            result = client.tools.getent.group(group)
            assert result is not None
            assert result.name == group
        if i == 0:
            client.sssd.stop()


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__disabled_intitgroups_getpwnam(client: Client, provider: GenericProvider):
    """
    :title: User is able to id(name) and id(uid) after 'memcache_size_initgroups' is set to '0' and SSSD is stopped
    :setup:
        1. Add users to SSSD
        2. Set users uids
        3. In SSSD nss change 'memcache_size_initgroups' to '0'
        4. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that users have correct names and uids
        3. Stop SSSD
        4. Find 'user1', 'user2' and 'user3' with id(name)
        5. Check that users have correct names and uids
        6. Find 'user1', 'user2' and 'user3' with id(uid)
        7. Check that users have correct names and uids
    :expectedresults:
        1. Users are found
        2. Users have correct names and uids
        3. SSSD is stopped
        4. Users are found
        5. Users have correct names and uids
        6. Users are found
        7. Users have correct names and uids
    :customerscenario: False
    """
    provider.user('user1').add(uid=10001)
    provider.user('user2').add(uid=10002)
    provider.user('user3').add(uid=10003)

    client.sssd.nss['memcache_size_initgroups'] = '0'
    client.sssd.start()

    for name, id in [('user1', 10001), ('user2', 10002), ('user3', 10003)]:
        result = client.tools.id(name)
        assert result is not None
        assert result.user.name == name
        assert result.user.id == id

    client.sssd.stop()

    for name, id in [('user1', 10001), ('user2', 10002), ('user3', 10003)]:
        result = client.tools.id(name)
        assert result is not None
        assert result.user.name == name
        assert result.user.id == id

        result = client.tools.id(id)
        assert result is not None
        assert result.user.name == name
        assert result.user.id == id


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__disabled_group(client: Client, provider: GenericProvider):
    """
    :title: User is able to id(name) and id(uid) after 'memcache_size_group' is set to '0' and SSSD is stopped,
            but groups are not able to getent.group()
    :setup:
        1. Add users to SSSD
        2. Set users uids
        3. Add groups to SSSD
        4. Set groups gids
        5. Add users to groups
        6. In SSSD nss change 'memcache_size_group' to '0'
        7. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that users have correct names
        3. Find 'group1' and 'group2' by getent.group(gid)
        4. Check that groups have correct gids and members
        5. Stop SSSD
        6. Find 'user1', 'user2' and 'user3' with id(name)
        7. Check that users have correct names
        8. Find 'group1' and 'group2' by getent.group(name)
        9. Find 'group1' and 'group2' by getent.group(gid)
    :expectedresults:
        1. Users are found
        2. Users have correct names
        3. Groups are found
        4. Groups have correct gids and members
        5. SSSD is stopped
        6. Users are found
        7. Users have correct names
        8. Groups are not found
        9. Groups are not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=10001)
    u2 = provider.user('user2').add(uid=10002)
    u3 = provider.user('user3').add(uid=10003)

    provider.group('group1').add(gid=1111).add_member(u1)
    provider.group('group2').add(gid=2222).add_members([u1, u2, u3])

    client.sssd.nss['memcache_size_group'] = '0'
    client.sssd.start()

    for user in ['user1', 'user2', 'user3']:
        result = client.tools.id(user)
        assert result is not None
        assert result.user.name == user

    for group, members in [(1111, ['user1']), (2222, ['user1', 'user2', 'user3'])]:
        result = client.tools.getent.group(group)
        assert result is not None
        assert result.gid == group
        assert result.members == members

    client.sssd.stop()

    for user in ['user1', 'user2', 'user3']:
        result = client.tools.id(user)
        assert result is not None
        assert result.user.name == user

    for group in ['group1', 'group2', 1111, 2222]:
        assert client.tools.id(group) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__disabled_cache(client: Client, provider: GenericProvider):
    """
    :title: User and group are not able to id() or getent.group() after SSSD is stopped and cache disabled
    :setup:
        1. Add users to SSSD
        2. Set users uids
        3. Add groups to SSSD
        4. Set groups gids
        5. Add users to groups
        6. In SSSD nss change 'memcache_size_passwd' to '0'
        7. In SSSD nss change 'memcache_size_group' to '0'
        8. In SSSD nss change 'memcache_size_initgroups' to '0'
        9. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that users have correct names
        3. Find 'group1' and 'group2' by getent.group(name)
        4. Check that groups have correct names and members
        5. Stop SSSD
        6. Find 'user1', 'user2' and 'user3' with id(name)
        7. Find 'user1', 'user2' and 'user3' with id(uid)
        8. Find 'group1' and 'group2' by getent.group(name)
        9. Find 'group1' and 'group2' by getent.group(gid)
    :expectedresults:
        1. Users are found
        2. Users have correct names
        3. Groups are found
        4. Groups have correct names and members
        5. SSSD is stopped
        6. Users are not found
        7. Users are not found
        8. Groups are not found
        9. Groups are not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=10001)
    u2 = provider.user('user2').add(uid=10002)
    u3 = provider.user('user3').add(uid=10003)

    provider.group('group1').add(gid=1111).add_member(u1)
    provider.group('group2').add(gid=2222).add_members([u1, u2, u3])

    client.sssd.nss['memcache_size_passwd'] = '0'
    client.sssd.nss['memcache_size_group'] = '0'
    client.sssd.nss['memcache_size_initgroups'] = '0'
    client.sssd.start()

    for user in ['user1', 'user2', 'user3']:
        result = client.tools.id(user)
        assert result is not None
        assert result.user.name == user

    for group, members in [('group1', ['user1']), ('group2', ['user1', 'user2', 'user3'])]:
        result = client.tools.getent.group(group)
        assert result is not None
        assert result.name == group
        assert result.members == members

    client.sssd.stop()

    for user in ['user1', 'user2', 'user3', 10001, 10002, 10003]:
        assert client.tools.id(user) is None

    for group in ['group1', 'group2', 1111, 2222]:
        assert client.tools.getent.group(group) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__membership_by_group_name(client: Client, provider: GenericProvider):
    """
    :title: User is able to id(name) and memberof([group]) after SSSD is stopped
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Add 'group1' and 'group2' to SSSD
        3. Add users to groups
        4. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that users are members of correct groups
        3. Stop SSSD
        4. Find 'user1', 'user2' and 'user3' with id(name)
        5. Check that users are members of correct groups
    :expectedresults:
        1. Users are found
        2. Users are members of correct groups
        3. SSSD is stopped
        4. Users are found
        5. Users are members of correct groups
    :customerscenario: False
    """
    u1 = provider.user('user1').add()
    u2 = provider.user('user2').add()
    u3 = provider.user('user3').add()

    provider.group('group1').add().add_member(u1)
    provider.group('group2').add().add_member(u1).add_member(u2).add_member(u3)

    client.sssd.start()

    for i in range(2):

        result = client.tools.id('user1')
        assert result is not None
        assert result.memberof(['group1', 'group2'])

        result = client.tools.id('user2')
        assert result is not None
        assert result.memberof(['group2'])

        result = client.tools.id('user3')
        assert result is not None
        assert result.memberof(['group2'])

        if i == 0:
            client.sssd.stop()


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__membership_by_group_id(client: Client, provider: GenericProvider):
    """
    :title: User is able to id(name) and memberof([gid]) after SSSD is stopped
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Add 'group1', 'group2' and 'group3' to SSSD
        3. Set group gids
        4. Add users to groups
        5. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that users are members of correct groups
        3. Stop SSSD
        4. Find 'user1', 'user2' and 'user3' with id(name)
        5. Check that users are members of correct groups
    :expectedresults:
        1. Users are found
        2. Users are members of correct groups
        3. SSSD is stopped
        4. Users are found
        5. Users are members of correct groups
    :customerscenario: False
    """
    u1 = provider.user('user1').add()
    u2 = provider.user('user2').add()
    u3 = provider.user('user3').add()

    provider.group('group1').add(gid=1001).add_member(u1)
    provider.group('group2').add(gid=1002).add_members([u1, u2, u3])
    provider.group('group3').add(gid=1003)

    client.sssd.start()

    for i in range(2):
        result = client.tools.id('user1')
        assert result is not None
        assert result.memberof([1001, 1002])

        result = client.tools.id('user2')
        assert result is not None
        assert result.memberof([1002])

        result = client.tools.id('user3')
        assert result is not None
        assert result.memberof([1002])

        if i == 0:
            client.sssd.stop()


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__user_gids(client: Client, provider: GenericProvider):
    """
    :title: User is able to id(uid) and memberof([gid]) after SSSD is stopped
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Set users uids and gids
        3. Add 'group1' and 'group2' to SSSD
        4. Set groups gids
        5. Add users to groups
        6. Start SSSD
    :steps:
        1. Find users using id(uid)
        2. Check that users are members of correct groups
        3. Stop SSSD
        4. Find users using id(uid)
        5. Check that users are members of correct groups
    :expectedresults:
        1. Users are found
        2. Users are members of correct groups
        3. SSSD is stopped
        4. Users are found
        5. Users are members of correct groups
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=2001, gid=101)
    u2 = provider.user('user2').add(uid=2002, gid=102)
    u3 = provider.user('user3').add(uid=2003, gid=103)

    provider.group('group1').add(gid=1001).add_member(u1)
    provider.group('group2').add(gid=1002).add_members([u1, u2, u3])

    client.sssd.start()

    for i in range(2):
        result = client.tools.id(2001)
        assert result is not None
        assert result.memberof([101, 1001, 1002])

        result = client.tools.id(2002)
        assert result is not None
        assert result.memberof([102, 1002])

        result = client.tools.id(2003)
        assert result is not None
        assert result.memberof([103, 1002])

        if i == 0:
            client.sssd.stop()


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__getpwnam_fully_qualified_names(client: Client, provider: GenericProvider):
    """
    :title: Resolving user with id(name@domain) when 'use_fully_qualified_names' is 'true' and sssd is stopped
    :setup:
        1. Add 'user1' and 'user2' to SSSD
        2. In SSSD domain change 'use_fully_qualified_names' to 'true'
        3. Start SSSD
    :steps:
        1. Find 'user1' and 'user2' with id(name)
        2. Find 'user1' and 'user2' with id(name@domain)
        3. Check that users have correct full names
        4. Stop SSSD
        5. Find 'user1' and 'user2' with id(name)
        6. Find 'user1' and 'user2' with id(name@domain)
        7. Check that users have correct full names
    :expectedresults:
        1. Users are not found
        2. Users are found
        3. Users have correct full names
        4. SSSD is stopped
        5. Users are not found
        6. Users are found
        7. Users have correct full names
    :customerscenario: False
    """
    u1 = provider.user('user1').add()
    u2 = provider.user('user2').add()

    client.sssd.domain['use_fully_qualified_names'] = 'true'
    client.sssd.start()

    for i in range(2):
        assert client.tools.id('user1') is None
        assert client.tools.id('user2') is None

        result = client.tools.id('user1@test')
        assert result is not None
        assert result.user.name == 'user1@test'

        result = client.tools.id('user2@test')
        assert result is not None
        assert result.user.name == 'user2@test'

        if i == 0:
            client.sssd.stop()


# NOT WORKING
@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__case_insensitive(client: Client, provider: GenericProvider):
    """
    :title: Resolving user by id(case_insensitive_name) when 'case_sensitive' is 'false' and SSSD is stopped
    :setup:
        1. Add 'user1' to SSSD
        2. Set user gid
        3. Add 'group1' to SSSD
        4. Set group gid
        5. Add member to the group
        6. In SSSD domain change 'case_sensitive' to 'false'
        7. Start SSSD
    :steps:
        1. Find users with id(name), where name is in random lower and upper case format
        2. Check that usernames are correct
        3. Check that users are members of correct groups
        4. Stop SSSD
        5. Find users with id(name), where name is last name used resolving user
        6. Check that username is correct
        7. Check that user is member of correct groups
        8. Find users with id(name), where names are previously used names
    :expectedresults:
        1. Users are found
        2. Users have correct names
        3. Users are members of correct groups
        4. SSSD is stopped
        5. Users is found
        6. User has correct name
        7. Users is member of correct groups
        7. Users are not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(gid=2001)
    provider.group('group1').add(gid=1001).add_members([u1])

    client.sssd.domain['case_sensitive'] = 'false'
    client.sssd.start()

    u1_groups = [2001, 1001]

    for name in ['uSer1', 'useR1', 'uSER1']:
        result = client.tools.id(name)
        assert result is not None
        assert result.user.name == name.lower()
        assert result.memberof(u1_groups)

    client.sssd.stop()

    result = client.tools.id('uSER1')
    assert result is not None
    assert result.user.name == name.lower()
    assert result.memberof(u1_groups)

    assert client.tools.id('uSer1') is None
    assert client.tools.id('useR1') is None


# NOT WORKING
@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__fq_names_case_insensitive(client: Client, provider: GenericProvider):
    """
    :title: User by id(), case insensitive fq name when 'case_sensitive' is 'false', 
            'use_fully_qualified_names' is 'true' and SSSD is stopped
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Set users gids
        3. Add 'group1', 'group2' and 'group3' to SSSD
        4. Set groups gids
        5. Add members to the groups
        6. In SSSD domain change 'use_fully_qualified_names' to 'true'
        7. In SSSD domain change 'case_sensitive' to 'false'
        8. Start SSSD
    :steps:
        1. Find user with id(name@domain), where name is in random lower and upper case format
        2. Check that user is members of correct groups
        3. Stop SSSD
        4. Find user with id(name@domain), where name is in random lower and upper case format
        5. Check that users are members of correct groups
        6. Find users with id(name)
    :expectedresults:
        1. User is found
        2. User is member of correct groups
        3. SSSD is stopped
        4. User is found
        5. User is member of correct groups
        6. Users are not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(gid=10100)
    u2 = provider.user('user2').add(gid=10200)
    u3 = provider.user('user3').add(gid=10300)

    provider.group('group1').add(gid=20001).add_members([u1])
    provider.group('group2').add(gid=20002).add_members([u1, u2])
    provider.group('group3').add(gid=20003).add_members([u1, u2, u3])

    client.sssd.domain['use_fully_qualified_names'] = 'true'
    client.sssd.domain['case_sensitive'] = 'false'
    client.sssd.start()

    result = client.tools.id('uSer1@test')
    assert result is not None
    assert result.memberof([10100, 20001, 20002, 20003])

    client.sssd.stop()

    result = client.tools.id('uSer1@test')
    assert result is not None
    assert result.memberof([10100, 20001, 20002, 20003])

    assert client.tools.id('user1') is None
    assert client.tools.id('user2') is None
    assert client.tools.id('user3') is None


# NOT WORKING
@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidatation_of_gids_after_initgroups(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(uid=10001, gid=1234)
    u2 = provider.user('user2').add(uid=10002, gid=102)

    provider.group('group1').add(gid=12345).add_member(u1)
    provider.group('group2').add(gid=1002).add_member(u2)

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.memberof([1234, 12345])

    result = client.tools.id(10001)
    assert result is not None
    assert result.memberof([1234, 12345])

    result = client.tools.getent.group('group1')
    assert result is not None
    assert result.name == 'group1'

    result = client.tools.getent.group('group2')
    assert result is not None
    assert result.name == 'group2'

    client.sssd.stop()

    result = client.tools.id('user1')
    assert result is not None
    assert result.memberof([1234, 12345])
    result = client.tools.id(10001)
    assert result is not None
    assert result.memberof([1234, 12345])

    result = client.tools.getent.group('group2')
    assert result is not None
    assert result.name == 'group2'
    result = client.tools.getent.group(1002)
    assert result is not None
    assert result.name == 'group2'

    result = client.tools.id('user1')
    assert result is not None
    assert result.memberof([1234, 12345])
    result = client.tools.id(10001)
    assert result is not None
    assert result.memberof([1234, 12345])

    assert client.tools.getent.group(1234) is None
    assert client.tools.getent.group(12345) is None
    assert client.tools.getent.group('group1') is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__initgroups_without_change_in_membership(client: Client, provider: GenericProvider):
    """
    :title: Cache expire without change in the membership
    :setup:
        1. Add 'user1' to SSSD
        2. Set user gid and uid
        3. Add 'group1' to SSSD
        4. Set group gid
        5. Add members to the group
        6. Start SSSD
    :steps:
        1. Find user with id(name) and id(uid)
        2. Check that user is member of correct groups
        3. Find group with getent.group(name) and getent.group(gid)
        4. Check that the group have correct name and gid
        5. Invalidate whole cache
        6. Find user with id(name) and id(uid)
        7. Check that user is member of correct groups
        8. Find group with getent.group(name) and getent.group(gid)
        9. Check that the group have correct name and gid
        10. Stop SSSD
        11. Find user with id(name) and id(uid)
        12. Check that user is member of correct groups
        13. Find group with getent.group(name) and getent.group(gid)
        14. Check that the group have correct name and gid
    :expectedresults:
        1. User is found
        2. User is member of correct groups
        3. Group is found
        4. Group has correct name and gid
        5. Cache is invalidated
        6. User is found
        7. User is member of correct groups
        8. Group is found
        9. Group has correct name and gid
        10. SSSD is stopped
        11. User is found
        12. User is member of correct groups
        13. Group is found
        14. Group has correct name and gid
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=10001, gid=111)
    provider.group('group1').add(gid=12345).add_member(u1)

    client.sssd.start()

    for i in range(3):
        result = client.tools.id('user1')
        assert result is not None
        assert result.memberof([111, 12345])

        result = client.tools.id(10001)
        assert result is not None
        assert result.memberof([111, 12345])

        result = client.tools.getent.group('group1')
        assert result is not None
        assert result.gid == 12345

        result = client.tools.getent.group(12345)
        assert result is not None
        assert result.name == 'group1'

        if i == 0:
            client.sssctl.cache_expire('-E')
        elif i == 1:
            client.sssd.stop()


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_user_before_stop(client: Client, provider: GenericProvider):
    """
    :title: Invalidate user cache before SSSD is stopped
    :setup:
        1. Add 'user1' and 'user2' to SSSD
        2. Set users gids and uids
        3. Add 'group1' and 'group2' to SSSD
        4. Set groups gids
        5. Add members to the groups
        6. Start SSSD
    :steps:
        1. Find user with id(name)
        2. Check that user has correct id
        3. Check that user is member of correct groups
        4. Invalidate cache for 'user1'
        5. Stop SSSD
        6. Find user by id(name) and id(uid)
        7. Find the user's groups by getent.group(name) and getent.group(uid)
    :expectedresults:
        1. User is found
        2. User has correct id
        3. User is member of correct groups
        4. Cache is invalidated
        5. SSSD is stopped
        6. User is not found
        7. Group is not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=123456, gid=110011)
    u2 = provider.user('user2').add(uid=220022, gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_members([u1, u2])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456
    assert result.memberof([110011, 101010, 202020])

    client.sssctl.cache_expire('-u', 'user1')
    client.sssd.stop()

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_user_after_stop(client: Client, provider: GenericProvider):
    """
    :title: Invalidate user cache after SSSD is stopped
    :setup:
        1. Add 'user1' and 'user2' to SSSD
        2. Set users gids and uids
        3. Add 'group1' and 'group2' to SSSD
        4. Set groups gids
        5. Add members to the groups
        6. Start SSSD
    :steps:
        1. Find user with id(name)
        2. Check that user has correct id
        3. Check that user is member of correct groups
        4. Stop SSSD
        5. Invalidate cache for 'user1'
        6. Find user by id(name) and id(uid)
        7. Find the user's groups by getent.group(name) and getent.group(uid)
    :expectedresults:
        1. User is found
        2. User has correct id
        3. User is member of correct groups
        4. SSSD is stopped
        5. Cache is invalidated
        6. User is not found
        7. Group is not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=123456, gid=110011)
    u2 = provider.user('user2').add(uid=220022, gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_members([u1, u2])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456
    assert result.memberof([110011, 101010, 202020])

    client.sssd.stop()
    client.sssctl.cache_expire('-u', 'user1')

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_users_before_stop(client: Client, provider: GenericProvider):
    """
    :title: Invalidate users cache before SSSD is stopped
    :setup:
        1. Add 'user1' and 'user2' to SSSD
        2. Set users gids and uids
        3. Add 'group1' and 'group2' to SSSD
        4. Set groups gids
        5. Add members to the groups
        6. Start SSSD
    :steps:
        1. Find users with id(name)
        2. Check that users have correct ids
        3. Check that users are members of correct groups
        4. Invalidate cache for all users
        5. Stop SSSD
        6. Find users by id(name) and id(uid)
        7. Find the groups of users by getent.group(name) and getent.group(uid)
    :expectedresults:
        1. Users are found
        2. Users have correct ids
        3. Users are members of correct groups
        4. Cache is invalidated
        5. SSSD is stopped
        6. Users are not found
        7. Groups are not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=123456, gid=110011)
    u2 = provider.user('user2').add(uid=220022, gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_members([u1, u2])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456
    assert result.memberof([110011, 101010, 202020])

    result = client.tools.id('user2')
    assert result is not None
    assert result.user.id == 220022
    assert result.memberof([222222, 202020])

    client.sssctl.cache_expire('-U')
    client.sssd.stop()

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None
    assert client.tools.id('user2') is None
    assert client.tools.id(220022) is None
    assert client.tools.getent.group(222222) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_users_after_stop(client: Client, provider: GenericProvider):
    """
    :title: Invalidate users cache after SSSD is stopped
    :setup:
        1. Add 'user1' and 'user2' to SSSD
        2. Set users gids and uids
        3. Add 'group1' and 'group2' to SSSD
        4. Set groups gids
        5. Add members to the groups
        6. Start SSSD
    :steps:
        1. Find users with id(name)
        2. Check that users have correct ids
        3. Check that users are members of correct groups
        4. Stop SSSD
        5. Invalidate cache for all users
        6. Find users by id(name) and id(uid)
        7. Find the groups of users by getent.group(name) and getent.group(uid)
    :expectedresults:
        1. Users are found
        2. Users have correct ids
        3. Users are members of correct groups
        4. SSSD is stopped
        5. Cache is invalidated
        6. Users are not found
        7. Groups are not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=123456, gid=110011)
    u2 = provider.user('user2').add(uid=220022, gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_members([u1, u2])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456
    assert result.memberof([110011, 101010, 202020])

    result = client.tools.id('user2')
    assert result is not None
    assert result.user.id == 220022
    assert result.memberof([222222, 202020])

    client.sssd.stop()
    client.sssctl.cache_expire('-U')

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None
    assert client.tools.id('user2') is None
    assert client.tools.id(220022) is None
    assert client.tools.getent.group(222222) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_group_before_stop(client: Client, provider: GenericProvider):
    """
    :title: Invalidate group cache before SSSD is stopped
    :setup:
        1. Add 'group1' to SSSD
        2. Set group gid
        3. Start SSSD
    :steps:
        1. Find the 'group1' getent.group(name)
        2. Check that group has correct id
        3. Check that group has correct name
        4. Invalidate cache for 'group1'
        5. Stop SSSD
        6. Find the 'group1' getent.group(name) and getent.group(uid)
    :expectedresults:
        1. Group is found
        2. Group has correct id
        3. Group has correct name
        4. Cache is invalidated
        5. SSSD is stopped
        6. Group is not found
    :customerscenario: False
    """
    provider.group('group1').add(gid=101010)

    client.sssd.start()

    result = client.tools.getent.group('group1')
    assert result is not None
    assert result.name == 'group1'
    assert result.gid == 101010

    client.sssctl.cache_expire('-g', 'group1')
    client.sssd.stop()

    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_group_after_stop(client: Client, provider: GenericProvider):
    """
    :title: Invalidate group cache after SSSD is stopped
    :setup:
        1. Add 'group1' to SSSD
        2. Set group gid
        3. Start SSSD
    :steps:
        1. Find the 'group1' getent.group(name)
        2. Check that group has correct id
        3. Check that group has correct name
        4. Stop SSSD
        5. Invalidate cache for 'group1'
        6. Find the 'group1' getent.group(name) and getent.group(uid)
    :expectedresults:
        1. Group is found
        2. Group has correct id
        3. Group has correct name
        6. SSSD is stopped
        5. Cache is invalidated
        6. Group is not found
    :customerscenario: False
    """
    provider.group('group1').add(gid=101010)

    client.sssd.start()

    result = client.tools.getent.group('group1')
    assert result is not None
    assert result.name == 'group1'
    assert result.gid == 101010

    client.sssd.stop()
    client.sssctl.cache_expire('-g', 'group1')

    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_groups_before_stop(client: Client, provider: GenericProvider):
    """
    :title: Invalidate groups cache before SSSD is stopped
    :setup:
        1. Add 'group1' and 'group2' to SSSD
        2. Set groups gids
        3. Start SSSD
    :steps:
        1. Find groups with getent.group(name)
        2. Check that groups have correct gids
        3. Invalidate cache for all groups
        4. Stop SSSD
        5. Find 'group1' and 'group2' with getent.group(name) and getent.group(gid)
    :expectedresults:
        1. Groups are found
        2. Groups have correct gids
        3. Cache is invalidated
        4. SSSD is stopped
        5. Groups are not found
    :customerscenario: False
    """
    provider.group('group1').add(gid=101010)
    provider.group('group2').add(gid=202020)

    client.sssd.start()

    result = client.tools.getent.group('group1')
    assert result is not None
    assert result.gid == 101010
    
    result = client.tools.getent.group('group2')
    assert result is not None
    assert result.gid == 202020

    client.sssctl.cache_expire('-G')
    client.sssd.stop()

    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_groups_after_stop(client: Client, provider: GenericProvider):
    """
    :title: Invalidate groups cache after SSSD is stopped
    :setup:
        1. Add 'group1' and 'group2' to SSSD
        2. Set groups gids
        3. Start SSSD
    :steps:
        1. Find groups with getent.group(name)
        2. Check that groups have correct gids
        3. Stop SSSD
        4. Invalidate cache for all groups
        5. Find 'group1' and 'group2' with getent.group(name) and getent.group(gid)
    :expectedresults:
        1. Groups are found
        2. Groups have correct gids
        3. SSSD is stopped
        4. Cache is invalidated
        5. Groups are not found
    :customerscenario: False
    """
    provider.group('group1').add(gid=101010)
    provider.group('group2').add(gid=202020)

    client.sssd.start()

    result = client.tools.getent.group('group1')
    assert result is not None
    assert result.gid == 101010
    
    result = client.tools.getent.group('group2')
    assert result is not None
    assert result.gid == 202020

    client.sssd.stop()
    client.sssctl.cache_expire('-G')

    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_everything_before_stop(client: Client, provider: GenericProvider):
    """
    :title: Invalidate all parts of cache before SSSD is stopped
    :setup:
        1. Add 'user1' and 'user2' to SSSD
        2. Set users uids and gids
        3. Add 'group1' and 'group2' to SSSD
        4. Set groups gids
        5. Add members to the groups
        6. Start SSSD
    :steps:
        1. Find users with id(name)
        2. Check that users have correct uids
        3. Find groups with getent.group(name)
        4. Check that groups have correct gids
        5. Invalidate all parts of cache
        6. Stop SSSD
        7. Find 'user1' and 'user2' with id(name) and id(uid)
        8. Find 'group1' and 'group2' with getent.group(name) and getent.group(gid)
    :expectedresults:
        1. Users are found
        2. Users have correct uids
        3. Groups are found
        4. Groups have correct gids
        5. Cache is invalidated
        6. SSSD is stopped
        7. Users are not found
        8. Groups are not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=123456, gid=110011)
    u2 = provider.user('user2').add(uid=220022, gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_members([u1, u2])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456

    result = client.tools.id('user2')
    assert result is not None
    assert result.user.id == 220022

    result = client.tools.getent.group('group1')
    assert result is not None
    assert result.gid == 101010
    
    result = client.tools.getent.group('group2')
    assert result is not None
    assert result.gid == 202020

    client.sssctl.cache_expire('-E')
    client.sssd.stop()

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.id('user2') is None
    assert client.tools.id(220022) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_everything_after_stop(client: Client, provider: GenericProvider):
    """
    :title: Invalidate all parts of cache after SSSD is stopped
    :setup:
        1. Add 'user1' and 'user2' to SSSD
        2. Set users uids and gids
        3. Add 'group1' and 'group2' to SSSD
        4. Set groups gids
        5. Add members to the groups
        6. Start SSSD
    :steps:
        1. Find users with id(name)
        2. Check that users have correct uids
        3. Find groups with getent.group(name)
        4. Check that groups have correct gids
        5. Stop SSSD
        6. Invalidate all parts of cache
        7. Find 'user1' and 'user2' with id(name) and id(uid)
        8. Find 'group1' and 'group2' with getent.group(name) and getent.group(gid)
    :expectedresults:
        1. Users are found
        2. Users have correct uids
        3. Groups are found
        4. Groups have correct gids
        5. SSSD is stopped
        6. Cache is invalidated
        7. Users are not found
        8. Groups are not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=123456, gid=110011)
    u2 = provider.user('user2').add(uid=220022, gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_members([u1, u2])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456

    result = client.tools.id('user2')
    assert result is not None
    assert result.user.id == 220022

    result = client.tools.getent.group('group1')
    assert result is not None
    assert result.gid == 101010
    
    result = client.tools.getent.group('group2')
    assert result is not None
    assert result.gid == 202020

    client.sssd.stop()
    client.sssctl.cache_expire('-E')

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.id('user2') is None
    assert client.tools.id(220022) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__memcache_timeout_zero(client: Client, provider: GenericProvider):
    """
    :title: Cache is not created at all when 'memcache_timeout' set to '0'
    :setup:
        1. Add 'user1' to SSSD
        2. Set user uid
        3. Add 'group1' to SSSD
        4. Set group gid
        5. In SSSD nss change 'memcache_timeout' set to '0'
        6. Start SSSD
    :steps:
        1. Check that cache is not created
        2. Find user with id(name)
        3. Check that user has correct uid
        4. Find group with getent.group(name)
        5. Check that group has correct gid
        6. Stop SSSD
        7. Find user with id(name) and id(uid)
        8. Find group with getent.group(name) and getent.group(gid)
    :expectedresults:
        1. Cache is not created
        2. User is found
        3. User has correct uid
        4. Group is found
        5. Group has correct gid
        6. Stop SSSD
        7. User is not found
        8. Group is not found
    :customerscenario: False
    """
    provider.user('user1').add(uid=123456)
    provider.group('group1').add(gid=10001)

    client.sssd.nss['memcache_timeout'] = '0'
    client.sssd.start()

    r = client.sssctl.cache_ls()
    assert r.stdout == ''
    assert r.stderr == ''

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456

    result = client.tools.getent.group('group1')
    assert result is not None
    assert result.gid == 10001

    client.sssd.stop()

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(10001) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__removed_cache_without_invalidation(client: Client, provider: GenericProvider):
    """
    :title: SSSD is stopped, cache removed then users and groups cannot be resolved
    :setup:
        1. Add 'user1' to SSSD
        2. Set user uid
        3. Add 'group1' to SSSD
        4. Set group gid
        5. Start SSSD
    :steps:
        1. Find user with id(name)
        2. Check that user has correct uid
        3. Find group with getent.group(name)
        4. Check that group has correct gid
        5. Stop SSSD
        6. Remove cache files
        7. Find user with id(name) and id(uid)
        8. Find group with getent.group(name) and getent.group(gid)
    :expectedresults:
        1. User is found
        2. User has correct uid
        3. Group is found
        4. Group has correct gid
        5. SSSD is stopped
        6. Cache files are removed
        7. User is not found
        8. Group is not found
    :customerscenario: True
    """
    provider.user('user1').add(uid=123456)
    provider.group('group1').add(gid=10001)

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456

    result = client.tools.getent.group('group1')
    assert result is not None
    assert result.gid == 10001

    client.sssd.stop()

    client.sssctl.remove_cache_files()

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(10001) is None
