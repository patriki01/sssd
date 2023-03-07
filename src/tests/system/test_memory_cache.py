import pytest

from lib.sssd.roles.ad import AD
from lib.sssd.roles.client import Client
from lib.sssd.roles.generic import GenericADProvider, GenericProvider
from lib.sssd.roles.ldap import LDAP
from lib.sssd.roles.samba import Samba
from lib.sssd.topology import KnownTopology, KnownTopologyGroup


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__getpwnam(client: Client, provider: GenericProvider):
    provider.user('user1').add(uid=1001)
    provider.user('user2').add(uid=1002)
    provider.user('user3').add(uid=1003)

    client.sssd.start()

    for user in ['user1', 'user2', 'user3']:
        result = client.tools.id(user)
        assert result is not None
        assert result.user.name == user
    
    client.sssd.stop()

    for user in ['user1', 'user2', 'user3']:
        result = client.tools.id(user)
        assert result is not None
        assert result.user.name == user


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__getgrnam(client: Client, provider: GenericProvider):
    provider.group('group1').add()
    provider.group('group2').add()
    provider.group('group3').add()

    client.sssd.start()

    for group in ['group1', 'group2', 'group3']:
        result = client.tools.getent.group(group)
        assert result is not None
        assert result.name == group

    client.sssd.stop()

    for group in ['group1', 'group2', 'group3']:
        result = client.tools.getent.group(group)
        assert result is not None
        assert result.name == group


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__getgrnam_disabled_passwd(client: Client, provider: GenericProvider):
    provider.group('group1').add()
    provider.group('group2').add()
    provider.group('group3').add()

    client.sssd.nss['memcache_size_passwd'] = '0'
    client.sssd.start()

    for group in ['group1', 'group2', 'group3']:
        result = client.tools.getent.group(group)
        assert result is not None
        assert result.name == group

    client.sssd.stop()

    for group in ['group1', 'group2', 'group3']:
        result = client.tools.getent.group(group)
        assert result is not None
        assert result.name == group


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__getgrnam_disabled_intitgroups(client: Client, provider: GenericProvider):
    provider.group('group1').add()
    provider.group('group2').add()
    provider.group('group3').add()

    client.sssd.nss['memcache_size_initgroups'] = '0'
    client.sssd.start()

    for group in ['group1', 'group2', 'group3']:
        result = client.tools.getent.group(group)
        assert result is not None
        assert result.name == group

    client.sssd.stop()

    for group in ['group1', 'group2', 'group3']:
        result = client.tools.getent.group(group)
        assert result is not None
        assert result.name == group


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_memory_cache__membership_by_group_name(client: Client, provider: GenericProvider):
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