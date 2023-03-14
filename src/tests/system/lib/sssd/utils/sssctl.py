
from pytest_mh import MultihostHost, MultihostUtility
from pytest_mh._private.multihost import MultihostRole
from pytest_mh.ssh import SSHLog, SSHProcess, SSHProcessResult


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

    def cache_expire(self, args: list[str]=None) -> None:
        """
        Run ``sssctl cache-expire`` command.

        :param args: Additional arguments, defaults to empty list.
        :type args: list[str], optional
        """
        if args is None:
            args = []
        self.host.ssh.exec(['sssctl', 'cache-expire', *args])


    