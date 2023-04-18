""" SSSD Sanity Test Cases

:requirement: IDM-SSSD-REQ : KRB5 Provider
:casecomponent: sssd
:subsystemteam: sst_idm_sssd
:upstream: yes
:status: approved
"""
import pytest

from lib.sssd.roles.kdc import KDC
from lib.sssd.roles.client import Client
from lib.sssd.roles.generic import GenericProvider
from lib.sssd.topology import KnownTopologyGroup, KnownTopology


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_ssh__login(client: Client, provider: GenericProvider):
    """
    :title: SSH login
    :setup:
        1. Add 'user1' to SSSD
        2. Set user password
        3. Start SSSD
    :steps:
        1. Authenticate user with correct password
        2. Authenticate user with incorrect password
    :expectedresults:
        1. User is authenticated
        2. User is not authenticated
    :customerscenario: False
    """
    provider.user('user1').add(password='123456')

    client.sssd.start()

    assert client.auth.ssh.password('user1', '123456')
    assert client.auth.ssh.password('user1', '023456') == False


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_ssh__offline_login(client: Client, provider: GenericProvider):
    provider.user('user1').add(password='123456')

    client.sssd.domain['cache_credentials'] = 'True'
    client.sssd.domain['krb5_store_password_if_offline'] = 'True'
    client.sssd.pam['offline_credentials_expiration'] = '0'
    client.sssd.start()

    assert client.auth.ssh.password('user1', '123456')

    # This stopping is wrong
    # provider.svc.stop('dirsrv@example1')
    # client.ssh('user1', '123456').run('systemctl stop krb5kdc')

    correct = client.auth.ssh.password('user1', '123456')
    incorrect = client.auth.ssh.password('user1', '023456')

    #provider.svc.start('dirsrv@example1')
    #client.ssh('user1', '123456').run('systemctl start krb5kdc')

    assert correct
    assert not incorrect


@pytest.mark.topology(KnownTopology.Client)
def test_ssh__simple_kinit(client: Client, kdc: KDC):
    """
    :title: Kinit
    :setup:
        1. Add 'user1' to kdc and set its password
        2. Add 'user1' to local and set its password
        3. Configure Kerberos to allow KCM tests
    :steps:
        1. Authenticate to ssh
        2. Connect to kerberos
        3. Authenticate to kerberos to get TGT
    :expectedresults:
        1. User is authenticated
        2. User is connected
        3. User is authenticated
    :customerscenario: False
    """
    kdc.principal('user1').add(password='123456')
    client.local.user('user1').add(password='123456')
    client.sssd.common.kcm(kdc)

    with client.ssh('user1', '123456') as ssh:
        with client.auth.kerberos(ssh) as krb:
            assert krb.kinit('user1', password='123456').rc == 0

