
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
        self.cache_path = '/var/lib/sss/mc'

    def cache_expire(self, *args: str) -> SSHProcessResult:
        """
        Run ``sssctl cache-expire`` command.

        :param args: Additional arguments.
        :type args: str
        """
        return self.host.ssh.exec(['sssctl', 'cache-expire', *args])

    def cache_ls(self) -> SSHProcessResult:
        """
        Run ``ls 'cache_path'`` command.
        Result output of ``ls`` is stored in result.stdout
        """
        return self.host.ssh.exec(['ls', self.cache_path])
    
    def remove_cache_files(self) -> SSHProcessResult:
        """
        Remove all cache files without invalidation.
        """
        r = self.cache_ls()
        for file in r.stdout.split():
            result = self.host.ssh.exec(['rm', f'{self.cache_path}/{file}'])
        return result
