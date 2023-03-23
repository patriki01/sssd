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
        2. Set their user ids
        3. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that results have correct names
        3. Check that results have correct ids
        4. Stop SSSD
        5. Find 'user1', 'user2' and 'user3' with id(name)
        6. Check that results have correct names
        7. Check that results have correct ids
    :expectedresults:
        1. Users are found
        2. Users have correct names
        3. Users have correct ids
        4. SSSDis stopped
        5. Users are found
        6. Users have correct names
        7. Users have correct ids
    :customerscenario: False
    """
    provider.user('user1').add(uid=1001)
    provider.user('user2').add(uid=1002)
    provider.user('user3').add(uid=1003)

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
    u1 = provider.user('user1').add(uid=10001)
    u2 = provider.user('user2').add(uid=10002)
    u3 = provider.user('user3').add(uid=10003)

    provider.group('group1').add(gid=1111).add_member(u1)
    provider.group('group2').add(gid=2222).add_members([u1, u2, u3])

    client.sssd.nss['memcache_size_passwd'] = '0'
    client.sssd.start()

    for group, members in [(1111, ['user1']), (2222, ['user1', 'user2', 'user3'])]:
        result = client.tools.getent.group(group)
        assert result is not None
        assert result.gid == group
        assert result.members == members

    for user in ['user1', 'user2', 'user3']:
        result = client.tools.id(user)
        assert result is not None
        assert result.user.name == user

    client.sssd.stop()

    for group, members in [(1111, ['user1']), (2222, ['user1', 'user2', 'user3'])]:
        result = client.tools.getent.group(group)
        assert result is not None
        assert result.gid == group
        assert result.members == members

    for user in ['user1', 'user2', 'user3']:
        assert client.tools.id(user) is None

    for user in [10001, 10002, 10003]:
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
    u1 = provider.user('user1').add(uid=10001)
    u2 = provider.user('user2').add(uid=10002)
    u2 = provider.user('user3').add(uid=10003)

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


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__disabled_group(client: Client, provider: GenericProvider):
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

    for group in ['group1', 'group2']:
        assert client.tools.id(group) is None

    for group in [1111, 2222]:
        assert client.tools.id(group) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__disabled_cache(client: Client, provider: GenericProvider):
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
        3. Add 'user1' to 'group1'
        4. Add 'user1', 'user2' and 'user3' to 'group2'
        5. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that results are members of correct groups using memberof([name])
        3. Stop SSSD
        4. Find 'user1', 'user2' and 'user3' with id(name)
        5. Check that results are members of correct groups using memberof([name])
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
        3. Set their gids
        4. Add 'user1' to 'group1'
        5. Add 'user1', 'user2' and 'user3' to 'group2'
        6. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that users are members of correct groups using memberof([gid])
        3. Stop SSSD
        4. Find 'user1', 'user2' and 'user3' with id(name)
        5. Check that users are members of correct groups using memberof([gid])
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
        4. Set their gids
        5. Add 'user1' to 'group1'
        6. Add 'user1', 'user2' and 'user3' to 'group2'
        7. Start SSSD
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
    :title: Resolving user with id(name@domain) only by fq name when 'use_fully_qualified_names' is 'true' and sssd is stopped
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


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__case_insensitive(client: Client, provider: GenericProvider):
    """
    :title: Resolving user by id() with case insensitive name when 'case_sensitive' is 'false' and sssd is stopped
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Set group ids to the users
        3. Add 'group1', 'group2' and 'group3' to SSSD
        4. Set them group ids.
        5. Add members to the groups
        6. In SSSD domain change 'case_sensitive' to 'false'
        7. Start SSSD
    :steps:
        1. Find users with id(name), where name is in random lower and upper case format
        2. Check that usernames are correctly set
        3. Check that users are members of correct groups
        4. Stop SSSD
        5. Find users with id(name), where name is in random lower and upper case format
        6. Check that usernames are correctly set
        7. Check that users are members of correct groups
    :expectedresults:
        1. Users are found
        2. Users have correctly set their names
        3. Users are members of correct groups
        4. SSSD is stopped
        5. Users are found
        6. Users have correctly set their names
        7. Users are members of correct groups
    :customerscenario: False
    """
    u1 = provider.user('user1').add(gid=2001)
    u2 = provider.user('user2').add(gid=2002)
    u3 = provider.user('user3').add(gid=2003)

    provider.group('group1').add(gid=1001).add_members([u1])
    provider.group('group2').add(gid=1002).add_members([u1, u2])
    provider.group('group3').add(gid=1003).add_members([u1, u2, u3])

    client.sssd.domain['case_sensitive'] = 'false'
    client.sssd.start()
    input('SSSD started')
    u1_groups = [2001, 1001, 1002, 1003]
    u2_groups = [2002, 1002, 1003]
    u3_groups = [2003, 1003]
    assert client.tools.id('User2')

    for name, groups in [('uSer1', u1_groups), ('useR1', u1_groups), ('uSER1', u1_groups)]:
        result = client.tools.id(name)
        assert result is not None
        assert result.user.name == name.lower()
        assert result.memberof(groups)
    input('before stop')

    client.sssd.stop()
    input('sssd Stopped')
    assert client.tools.id('uSer1') is None
    assert client.tools.id('useR1') is None

    result = client.tools.id('uSER1')
    assert result is not None
    assert result.user.name == name.lower()
    assert result.memberof(u1_groups)


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__fq_names_case_insensitive(client: Client, provider: GenericProvider):
    """
    :title: User by id(), case insensitive fq name when 'case_sensitive' is 'false', 
            'use_fully_qualified_names' is 'true' and SSSD is stopped
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Set them group ids
        3. Add 'group1', 'group2' and 'group3' to SSSD
        4. Set them group ids
        5. Add members to the groups
        6. In SSSD domain change 'use_fully_qualified_names' to 'true'
        7. In SSSD domain change 'case_sensitive' to 'false'
        8. Start SSSD
    :steps:
        1. Find users with id(name@domain), where name is in random lower and upper case format
        2. Check that users are members of correct groups
        3. Stop SSSD
        4. Find users with id(name), where name is in random lower and upper case format
        5. Check that users are members of correct groups
        6. Find users with id(name)
    :expectedresults:
        1. Users are found
        2. Users are members of correct groups
        3. SSSD is stopped
        4. Users are found
        5. Users are members of correct groups
        6. Users are not found
    :customerscenario: False
    """
    u1 = provider.user('user1').add(gid=101)
    u2 = provider.user('user2').add(gid=102)
    u3 = provider.user('user3').add(gid=103)

    provider.group('group1').add(gid=1001).add_members([u1])
    provider.group('group2').add(gid=1002).add_members([u1, u2])
    provider.group('group3').add(gid=1003).add_members([u1, u2, u3])

    client.sssd.domain['use_fully_qualified_names'] = 'true'
    client.sssd.domain['case_sensitive'] = 'false'
    client.sssd.start()

    result = client.tools.id('uSer1@test', '-G')
    assert result is not None
    assert result.memberof([101, 1001, 1002, 1003])

    client.sssd.stop()

    result = client.tools.id('uSer1@test', '-G')
    assert result is not None
    assert result.memberof([101, 1001, 1002, 1003])

    assert client.tools.id('user1') is None
    assert client.tools.id('user2') is None
    assert client.tools.id('user3') is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidatation_of_gids_after_initgroups(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(uid=10001, gid=1234)
    u2 = provider.user('user2').add(uid=10002, gid=102)

    provider.group('group1').add(gid=12345).add_member(u1)
    provider.group('group2').add(gid=1002).add_member(u2)

    client.sssd.start()##################################### SETUP

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

    client.sssd.stop()###################################### STOP

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

    #assert_initgroups_equal()#####################################????????
    result = client.tools.id('user1')
    assert result is not None
    assert result.memberof([1234, 12345])
    result = client.tools.id(10001)
    assert result is not None
    assert result.memberof([1234, 12345])

    assert client.tools.getent.group(1234) is None # Tohle projde
    assert client.tools.getent.group(12345) is None # Tohle uz neprojde
    assert client.tools.getent.group('group1') is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__initgroups_without_change_in_membership(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(uid=10001, gid=101)
    u2 = provider.user('user2').add(uid=10002, gid=202)

    provider.group('group1').add(gid=1001).add_member(u1)
    provider.group('group2').add(gid=2002).add_member(u2)

    client.sssd.start()

    for i in range(3):
        result = client.tools.id('user1')
        assert result is not None
        assert result.memberof([101, 1001])

        assert client.tools.getent.group('group1') is not None
        assert client.tools.getent.group('group1').gid == 1001

        result = client.tools.id(10002)
        assert result is not None
        assert result.memberof([202, 2002])

        assert client.tools.getent.group(2002) is not None
        assert client.tools.getent.group(2002).name == 'group2'

        if i == 0:
            client.sssctl.cache_expire('-E')
        elif i == 1:
            client.sssd.stop()


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_user_before_stop(client: Client, provider: GenericProvider):
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
    u1 = provider.user('user1').add(uid=123456, gid=110011)
    u2 = provider.user('user2').add(uid=220022, gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_members([u1, u2])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456
    assert result.memberof([110011, 101010, 202020])

    client.sssctl.cache_expire('-U')
    client.sssd.stop()

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_users_after_stop(client: Client, provider: GenericProvider):
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
    client.sssctl.cache_expire('-U')

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_group_before_stop(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(uid=123456, gid=110011)
    u2 = provider.user('user2').add(uid=220022, gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_members([u1, u2])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456
    assert result.memberof([110011, 101010, 202020])

    client.sssctl.cache_expire('-g', 'group1')
    client.sssd.stop()

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None



@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_group_after_stop(client: Client, provider: GenericProvider):
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
    client.sssctl.cache_expire('-g', 'group1')

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_groups_before_stop(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(uid=123456, gid=110011)
    u2 = provider.user('user2').add(uid=220022, gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_members([u1, u2])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456
    assert result.memberof([110011, 101010, 202020])

    client.sssctl.cache_expire('-G')
    client.sssd.stop()

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_groups_after_stop(client: Client, provider: GenericProvider):
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
    client.sssctl.cache_expire('-G')

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_everything_before_stop(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(uid=123456, gid=110011)
    u2 = provider.user('user2').add(uid=220022, gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_members([u1, u2])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.user.id == 123456
    assert result.memberof([110011, 101010, 202020])

    client.sssctl.cache_expire('-E')
    client.sssd.stop()

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_everything_after_stop(client: Client, provider: GenericProvider):
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
    client.sssctl.cache_expire('-E')

    assert client.tools.id('user1') is None
    assert client.tools.id(123456) is None
    assert client.tools.getent.group('group1') is None
    assert client.tools.getent.group(110011) is None
    assert client.tools.getent.group('group2') is None
    assert client.tools.getent.group(202020) is None
