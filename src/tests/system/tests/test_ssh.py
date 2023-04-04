import pytest

from lib.sssd.roles.client import Client
from lib.sssd.roles.generic import GenericProvider
from lib.sssd.topology import KnownTopologyGroup


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_ssh__login(client: Client, provider: GenericProvider):
    """
    :title: Ssh login
    :setup:
        1. Add 'user1' to SSSD
        2. Set user password
        3. Start SSSD
    :steps:
        1. Authenticate user with correct password
        2. Authenticate user with Kerberos credentials
        3. Authenticate user with incorrect password
    :expectedresults:
        1. User is authenticated
        2. User is authenticated
        3. User is not authenticated
    :customerscenario: False
    """
    provider.user('user1').add(password='123456')

    client.sssd.start()

    assert client.auth.ssh.password('user1', '123456')
    # assert client.auth.ssh.password('foo1', 'Secret123')
    assert client.auth.ssh.password('user1', '023456') == False


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_ssh__offline_login(client: Client, provider: GenericProvider):
    provider.user('user1').add()

    client.sssd.domain['cache_credentials'] = 'True'
    client.sssd.domain['krb5_store_password_if_offline'] = 'True'
    client.sssd.pam['offline_credentials_expiration'] = '0'
    client.sssd.start()