import pytest
import subprocess

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
def test_memory_cache__getgrnam_disabled_passwd(client: Client, provider: GenericProvider):
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
def test_memory_cache__getgrnam_disabled_intitgroups(client: Client, provider: GenericProvider):
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

        result=client.tools.id('user1')
        assert result is not None
        assert result.memberof(['group1', 'group2'])

        result=client.tools.id('user2')
        assert result is not None
        assert result.memberof(['group2'])

        result=client.tools.id('user3')
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
        assert result.memberof([1001,1002])

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


#dont have converted mark
@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__case_insensitive(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(gid=101)
    u2 = provider.user('user2').add(gid=102)
    u3 = provider.user('user3').add(gid=103)

    provider.group('group1').add(gid=1001).add_members([u1])
    provider.group('group2').add(gid=1002).add_members([u1, u2])
    provider.group('group3').add(gid=1003).add_members([u1, u2, u3])

    client.sssd.domain['case_sensitive'] = 'false'
    client.sssd.start()

    u1_groups = [101, 1001, 1002, 1003]
    u2_groups = [102, 1002, 1003]
    u3_groups = [103, 1003]

    for i in range(2):
        for name, groups in [('uSer1', u1_groups), ('useR1', u1_groups), ('uSER1', u1_groups), 
                            ('USEr2', u2_groups), ('uSEr2', u2_groups), ('usER2', u2_groups),
                            ('USer3', u3_groups), ('uSer3', u3_groups), ('USER3', u3_groups),]:
            result = client.tools.id(name)
            assert result is not None
            assert result.user.name == name.lower()
            assert result.memberof(groups)
        if i == 0:
            client.sssd.stop()


# TODO STILL NOT WORKING WHEN SSSD IS STOPPED
@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__fq_names_case_insensitive(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(gid=101)
    u2 = provider.user('user2').add(gid=102)
    u3 = provider.user('user3').add(gid=103)

    provider.group('group1').add(gid=1001).add_members([u1])
    provider.group('group2').add(gid=1002).add_members([u1, u2])
    provider.group('group3').add(gid=1003).add_members([u1, u2, u3])

    client.sssd.domain['use_fully_qualified_names'] = 'true'
    client.sssd.domain['case_sensitive'] = 'false'
    client.sssd.start()

    for i in range(2):
        result = client.tools.id('user1@test')
        assert result is not None
        assert result.memberof([101, 1001, 1002, 1003])

        result = client.tools.id('uSeR2@test')
        assert result is not None
        assert result.memberof([102, 1002, 1003])

        result = client.tools.id('UsER3@tEst')
        assert result is not None
        assert result.memberof([103, 1003])

        if i == 0:
            client.sssd.stop()


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_user_before_stop(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(gid=110011)
    u2 = provider.user('user2').add(uid=220022,gid=222222)

    provider.group('group1').add(gid=101010).add_member(u1)
    provider.group('group2').add(gid=202020).add_member(u2)

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.memberof([110011, 101010])

    result = client.tools.id('user2')
    assert result is not None
    assert result.memberof([222222, 202020])

    client.sssctl.cache_expire(['-u', 'user1'])
    client.sssd.stop()

    assert client.tools.id('user1') is None
    assert client.tools.getent.group(101010) is None

    result = client.tools.id(220022)
    assert result is not None
    assert result.memberof([222222, 202020])


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__invalidate_user_after_stop(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(gid=101)
    u2 = provider.user('user2').add(gid=202)

    provider.group('group1').add(gid=1001).add_member(u1)
    provider.group('group2').add(gid=2002).add_member(u2)

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.memberof([101, 1001])

    result = client.tools.id('user2')
    assert result is not None
    assert result.memberof([202, 2002])

    client.sssd.stop()
    client.sssctl.cache_expire(['-u', 'user1'])

    assert client.tools.id('user1') is None
    assert client.tools.getent.group(101) is None

    result = client.tools.id('user2')
    assert result is not None
    assert result.memberof([202, 2002])

