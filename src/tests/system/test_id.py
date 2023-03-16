import pytest

from lib.sssd.roles.ad import AD
from lib.sssd.roles.client import Client
from lib.sssd.roles.generic import GenericADProvider, GenericProvider
from lib.sssd.roles.ldap import LDAP
from lib.sssd.roles.samba import Samba
from lib.sssd.topology import KnownTopology, KnownTopologyGroup


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__getpwnam(client: Client, provider: GenericProvider):
    """
    :title: Resolving user with getpwnam by id(name) utility
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Set their user ids
        3. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that results have correct names
        3. Check that results have correct ids
    :expectedresults:
        1. Users are found
        2. Users have correct names
        3. Users have correct ids
    :customerscenario: False
    """
    provider.user('user1').add(uid=1001)
    provider.user('user2').add(uid=1002)
    provider.user('user3').add(uid=1003)

    client.sssd.start()

    for name, uid in [('user1', 1001), ('user2', 1002), ('user3', 1003)]:
        result = client.tools.id(name)
        assert result is not None
        assert result.user.name == name
        assert result.user.id == uid


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__getpwuid(client: Client, provider: GenericProvider):
    """
    :title: Resolving user with getpwuid by id(uid) utility
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Set their user ids
        3. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id() by user id
        2. Check that results have correct names
        3. Check that results have correct ids
    :expectedresults:
        1. Users are found
        2. Users have correct names
        3. Users have correct ids
    :customerscenario: False
    """
    provider.user('user1').add(uid=1001)
    provider.user('user2').add(uid=1002)
    provider.user('user3').add(uid=1003)

    client.sssd.start()

    for name, uid in [('user1', 1001), ('user2', 1002), ('user3', 1003)]:
        result = client.tools.id(uid)
        assert result is not None
        assert result.user.name == name
        assert result.user.id == uid


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__getgrnam(client: Client, provider: GenericProvider):
    """
    :title: Resolving group with getgrnam by getent.group(name) utility
    :setup:
        1. Add 'group1', 'group2' and 'group3' to SSSD
        2. Set their group ids
        3. Start SSSD
    :steps:
        1. Find 'group1', 'group2' and 'group3' with getent.group(name)
        2. Check that groups have correct names
        3. Check that groups have correct group ids
    :expectedresults:
        1. Groups are found
        2. Groups have correct names
        3. Groups have correct ids
    :customerscenario: False
    """    
    provider.group('group1').add(gid=1001)
    provider.group('group2').add(gid=1002)
    provider.group('group3').add(gid=1003)

    client.sssd.start()

    for name, gid in [('group1', 1001), ('group2', 1002), ('group3', 1003)]:
        result = client.tools.getent.group(name)
        assert result is not None
        assert result.name == name
        assert result.gid == gid


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__getgrgid(client: Client, provider: GenericProvider):
    """
    :title: Resolving group with getgrgid by getent.group(gid) utility
    :setup:
        1. Add 'group1', 'group2' and 'group3' to SSSD
        2. Set their group ids
        3. Start SSSD
    :steps:
        1. Find 'group1', 'group2' and 'group3' with getent.group() by group id
        2. Check that results have correct names
        3. Check that results have correct group ids
    :expectedresults:
        1. Groups are found
        2. Groups have correct names
        3. Groups have correct ids
    :customerscenario: False
    """    
    provider.group('group1').add(gid=1001)
    provider.group('group2').add(gid=1002)
    provider.group('group3').add(gid=1003)

    client.sssd.start()

    for name, gid in [('group1', 1001), ('group2', 1002), ('group3', 1003)]:
        result = client.tools.getent.group(gid)
        assert result is not None
        assert result.name == name
        assert result.gid == gid


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__getent_passwd(client: Client, provider: GenericProvider):
    """
    :title: Resolving user by getent.passwd() utility
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Set their user ids
        3. Add 'group1', 'group2' and 'group3' to SSSD
        4. Add users to groups
        5. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with getent(name)
        2. Find 'user1', 'user2' and 'user3' with getent(uid)
        3. Check that users have correct names
        4. Check that users have correct ids
    :expectedresults:
        1. Users are found
        2. Users are found
        3. Users have correct names
        4. Users have correct ids
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=10001)
    u2 = provider.user('user2').add(uid=10002)
    u3 = provider.user('user3').add(uid=10003)

    provider.group('group1').add().add_member(u1)
    provider.group('group2').add().add_members([u1, u2])
    provider.group('group3').add().add_members([u1, u2, u3])

    client.sssd.start()

    assert client.tools.getent.passwd('user1').uid == 10001
    assert client.tools.getent.passwd(10001).name == 'user1'
    assert client.tools.getent.passwd('user2').uid == 10002
    assert client.tools.getent.passwd(10002).name == 'user2'
    assert client.tools.getent.passwd('user3').uid == 10003
    assert client.tools.getent.passwd(10003).name == 'user3'


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__getent_group(client: Client, provider: GenericProvider):
    """
    :title: Resolving user by getent.group() utility
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Add 'group1', 'group2' and 'group3' to SSSD
        3. Set their gids
        4. Add users to groups
        5. Start SSSD
    :steps:
        1. Find 'group1', 'group2' and 'group3' with getent(name)
        2. Find 'group1', 'group2' and 'group3' with getent(gid)
        3. Check that groups have correct names
        4. Check that groups have correct users added
    :expectedresults:
        1. Groups are found
        2. Groups are found
        3. Groups have correct names
        4. Groups have correct users added
    :customerscenario: False
    """
    u1 = provider.user('user1').add()
    u2 = provider.user('user2').add()
    u3 = provider.user('user3').add()

    provider.group('group1').add(gid=10001).add_member(u1)
    provider.group('group2').add(gid=10002).add_members([u1, u2])
    provider.group('group3').add(gid=10003).add_members([u1, u2, u3])

    client.sssd.start()

    assert client.tools.getent.group('group1').members == ['user1']
    assert client.tools.getent.group(10001).name == 'group1'
    assert client.tools.getent.group(10001).members == ['user1']
    assert client.tools.getent.group('group2').members == ['user1', 'user2']
    assert client.tools.getent.group(10002).name == 'group2'
    assert client.tools.getent.group(10002).members == ['user1', 'user2']
    assert client.tools.getent.group('group3').members == ['user1', 'user2', 'user3']
    assert client.tools.getent.group(10003).name == 'group3'
    assert client.tools.getent.group(10003).members == ['user1', 'user2', 'user3']


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__membership_by_group_name(client: Client, provider: GenericProvider):
    """
    :title: Resolving that user is member of group with id(name) utility and memberof([name])
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Add 'group1' and 'group2' to SSSD
        3. Add 'user1' to 'group1'
        4. Add 'user1', 'user2' and 'user3' to 'group2'
        3. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that users are members of correct groups using memberof([name])
    :expectedresults:
        1. Users are found
        2. Users are members of correct groups
    :customerscenario: False
    """
    u1 = provider.user('user1').add()
    u2 = provider.user('user2').add()
    u3 = provider.user('user3').add()

    provider.group('group1').add().add_member(u1)
    provider.group('group2').add().add_members([u1, u2, u3])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.memberof(['group1', 'group2'])

    result = client.tools.id('user2')
    assert result is not None
    assert result.memberof(['group2'])

    result = client.tools.id('user3')
    assert result is not None
    assert result.memberof(['group2'])


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__membership_by_group_id(client: Client, provider: GenericProvider):
    """
    :title: Resolving that user is member of group with id(name) utility and memberof([gid])
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Add 'group1', 'group2' and 'group3' to SSSD
        3. Add 'user1' to 'group1'
        4. Add 'user1', 'user2' and 'user3' to 'group2'
        5. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id(name)
        2. Check that users are members of correct groups using memberof([gid])
    :expectedresults:
        1. Users are found
        2. Users are members of correct groups
    :customerscenario: False
    """
    u1 = provider.user('user1').add()
    u2 = provider.user('user2').add()
    u3 = provider.user('user3').add()

    provider.group('group1').add(gid=1001).add_member(u1)
    provider.group('group2').add(gid=1002).add_members([u1, u2, u3])
    provider.group('group3').add(gid=1003)

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.memberof([1001,1002])

    result = client.tools.id('user2')
    assert result is not None
    assert result.memberof([1002])

    result = client.tools.id('user3')
    assert result is not None
    assert result.memberof([1002])


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__user_gids(client: Client, provider: GenericProvider):
    """
    :title: User is member of correct group using id(uid) and memberof([gid])
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
        2. Users should be members of correct groups
    :expectedresults:
        1. Users are found
        2. Users are members of correct groups
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=2001, gid=101)
    u2 = provider.user('user2').add(uid=2002, gid=102)
    u3 = provider.user('user3').add(uid=2003, gid=103)

    provider.group('group1').add(gid=1001).add_member(u1)
    provider.group('group2').add(gid=1002).add_members([u1, u2, u3])

    client.sssd.start()

    result = client.tools.id(2001)
    assert result is not None
    assert result.memberof([101, 1001, 1002])

    result = client.tools.id(2002)
    assert result is not None
    assert result.memberof([102, 1002])

    result = client.tools.id(2003)
    assert result is not None
    assert result.memberof([103, 1002])


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__getpwnam_fully_qualified_names(client: Client, provider: GenericProvider):
    """
    :title: User can be resolved with id() only by fq name when 'use_fully_qualified_names' is 'true'
    :setup:
        1. Add 'user1' and 'user2' to SSSD
        2. Set their user ids
        3. In SSSD domain change 'use_fully_qualified_names' to 'true'
        4. Start SSSD
    :steps:
        1. Find 'user1' and 'user2' with id(name)
        2. Find 'user1' and 'user2' with id(name@domain)
        3. Check that users have correct full names
        4. Check that users have correct ids
    :expectedresults:
        1. Users are not found
        2. Users are found
        3. Users have correct full names
        4. Users have correct ids
    :customerscenario: False
    """
    u1 = provider.user('user1').add(uid=10001)
    u2 = provider.user('user2').add(uid=10002)

    client.sssd.domain['use_fully_qualified_names'] = 'true'
    client.sssd.start()
        
    assert client.tools.id('user1') is None
    assert client.tools.id('user2') is None

    result = client.tools.id('user1@test')
    assert result is not None
    assert result.user.name == 'user1@test'
    assert result.user.id == 10001

    result = client.tools.id('user2@test')
    assert result is not None
    assert result.user.name == 'user2@test'
    assert result.user.id == 10002


#dont have converted mark
@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__case_insensitive(client: Client, provider: GenericProvider):
    """
    :title: Resolving user by id() with case insensitive name when 'case_sensitive' is 'false'
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
    :expectedresults:
        1. Users are found
        2. Users have correct names
        3. Users are members of correct groups
    :customerscenario: False
    """
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

    for name, groups in [('uSer1', u1_groups), ('useR1', u1_groups), ('uSER1', u1_groups), 
                         ('USEr2', u2_groups), ('uSEr2', u2_groups), ('usER2', u2_groups),
                         ('USer3', u3_groups), ('uSer3', u3_groups), ('USER3', u3_groups),]:
        result = client.tools.id(name)
        assert result is not None
        assert result.user.name == name.lower()
        assert result.memberof(groups)


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__fq_names_case_insensitive(client: Client, provider: GenericProvider):
    """
    :title: Resolving user by id() with fq case insensitive name when 'case_sensitive' is 'false' and 'use_fully_qualified_names' is 'true'
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
        1. Find users with id(name)
        2. Find users with id(name@domain) - name is in random lower and upper case format
        3. Check that users have correct groups
    :expectedresults:
        1. Users are not found
        2. Users are found
        3. Users are members of correct groups
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

    assert client.tools.id('user1') is None
    assert client.tools.id('user2') is None
    assert client.tools.id('user3') is None

    for name in ['User1@TesT', 'UseR1@TesT', 'UsER1@TesT']:
        result = client.tools.id(name)
        assert result is not None
        assert result.memberof([101, 1001, 1002, 1003])

    for name in ['uSer2@TeST', 'user2@TEsT', 'uSER2@tesT']:
        result = client.tools.id(name)
        assert result is not None
        assert result.memberof([102, 1002, 1003])

    for name in ['USer3@TeST', 'uSer3@TeST', 'USER3@Test']:
        result = client.tools.id(name)
        assert result is not None
        assert result.memberof([103, 1003])
    