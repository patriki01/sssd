
from pytest_mh import MultihostHost, MultihostUtility
from pytest_mh.ssh import SSHProcessResult


class SSSCTLUtils(MultihostUtility[MultihostHost]):
    """
    Manage and configure cache.

    """
    def __init__(self, host: MultihostHost ) -> None:
        """
        :param host: Multihost host.
        :type host: MultihostHost
        """ """"""
        super().__init__(host)

    def cache_expire(self, *args: str) -> SSHProcessResult:
        """
        Run ``sssctl cache-expire`` command.

        :param args: Additional arguments.
        :type args: str
        """
        return self.host.ssh.exec(['sssctl', 'cache-expire', *args])
