""" SSSD Configuration-related Test Cases

:requirement: IDM-SSSD-REQ: Configuration merging
:casecomponent: sssd
:subsystemteam: sst_idm_sssd
:upstream: yes
:status: approved
"""

import pytest

from sssd_test_framework.sssd.roles.client import Client
from sssd_test_framework.sssd.topology import KnownTopologyGroup


@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_config__change_config_while_sssd_running(client: Client):
    client.sssd.pam['debug_level'] = '9'
    client.sssd.start()

    assert 'debug_level = 9' in client.sssd.config_dumps()
    client.sssd.pam['debug_level'] = '1'
    assert client.sssd.pam['debug_level'] == '1'












@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_config__change_particular_section(client: Client):
    client.sssd.pam['debug_level'] = '9'
    client.sssd.nss['debug_level'] = '9'
    client.sssd.start()

    assert client.sssd.pam['debug_level'] == '9'
    assert client.sssd.nss['debug_level'] == '9'

    client.sssd.pam['debug_level'] = '1'
    client.sssd.nss['debug_level'] = '1'

    assert client.sssd.pam['debug_level'] == '1'
    assert client.sssd.nss['debug_level'] == '1'



















# Done
@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_config__add_remove_section(client: Client):
    client.sssd.pam['debug_level'] = '9'
    client.sssd.nss['debug_level'] = '9'
    client.sssd.start()
    assert client.sssd.pam['debug_level'] == '9'
    assert client.sssd.nss['debug_level'] == '9'

    client.sssd.config['new_section'] = {'key' : 'value'}

    assert 'key = value' in client.sssd.config_dumps()

    del client.sssd.config['new_section']

    assert 'key = value' not in client.sssd.config_dumps()

    assert client.sssd.pam['debug_level'] == '9'
    assert client.sssd.nss['debug_level'] == '9'









# Done
@pytest.mark.topology(KnownTopologyGroup.AnyProvider)
def test_config__genconf_no_such_section(client: Client):
    """
    :title: genconf with no existing section did not fail
    :setup:
        1. Start SSSD
    :steps:
        1. Authenticate to ssh
        2. Call 'sssd --genconf-section=$nonexistingSection'
    :expectedresults:
        1. User is authenticated
        2. Call did not fail
    :customerscenario: False
    """
    client.sssd.start()
    with client.ssh('ci', 'Secret123') as ssh:
        assert (ssh.run('/usr/sbin/sssd --genconf-section=xf31deyz')).rc == 0    