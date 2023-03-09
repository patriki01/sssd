from typing import List

from pytest_mh import MultihostHost, MultihostUtility
from pytest_mh._private.multihost import MultihostRole
from pytest_mh.ssh import SSHLog, SSHProcess, SSHProcessResult


class SSSCTLUtils(MultihostUtility[MultihostHost]):

    def __init__(self, host: MultihostHost ) -> None:
        super().__init__(host)
        self.host = host

    def cache_expire(self, options: List[str]=[]) -> SSHProcessResult:
        return self.host.ssh.exec(['sssctl', 'cache-expire'] + options)
