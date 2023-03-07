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
    :title: Resolving user with getpwnam by id() utility
    :setup:
        1. Add 'user1', 'user2' and 'user3' to SSSD
        2. Set their user ids
        3. Start SSSD
    :steps:
        1. Find 'user1', 'user2' and 'user3' with id() by name
        2. Check that result have correct names
        3. Check that result have correct id
    :expectedresults:
        1. Users are found
        2. Users have correct names
        3. Users have correct id
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
def test_id__membership_by_group_name(client: Client, provider: GenericProvider):
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
def test_id__getpwnam_fully_qualified_names(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add()
    u2 = provider.user('user2').add()

    client.sssd.domain['use_fully_qualified_names'] = 'true'
    client.sssd.start()
        
    assert client.tools.id('user1') is None
    assert client.tools.id('user2') is None

    result = client.tools.id('user1@test')
    assert result is not None
    assert result.user.name == 'user1@test'

    result = client.tools.id('user2@test')
    assert result is not None
    assert result.user.name == 'user2@test'


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__user_gids(client: Client, provider: GenericProvider):
    u1 = provider.user('user1').add(gid=101)
    u2 = provider.user('user2').add(gid=102)
    u3 = provider.user('user3').add(gid=103)

    provider.group('group1').add(gid=1001).add_member(u1)
    provider.group('group2').add(gid=1002).add_members([u1, u2, u3])

    client.sssd.start()

    result = client.tools.id('user1')
    assert result is not None
    assert result.memberof([101, 1001, 1002])

    result = client.tools.id('user2')
    assert result is not None
    assert result.memberof([102, 1002])

    result = client.tools.id('user3')
    assert result is not None
    assert result.memberof([103, 1002])


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_id__fq_names_case_insensitive(client: Client, provider: GenericProvider):
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
    