import os


class UnixUser:
    def __init__(self, home: str, username: str, user_runtime_tmp_path: str, uid: int, gid: int):
        self._home = home
        self._username = username
        self._user_runtime_tmp_path = user_runtime_tmp_path
        self._uid = uid
        self._gid = gid

    def home(self) -> str:
        """Home directory of the current user

        :return: path to home directory
        """
        return self._home

    def username(self) -> str:
        """Name of the current user

        :return: current user name
        """
        return self._username

    def user_runtime_tmp_path(self) -> str:
        return self._user_runtime_tmp_path

    def uid(self) -> int:
        """UID of the current user

        :return: current user UID
        """
        return self._uid

    def gid(self) -> int:
        """GID of the current user

        :return: current user GID
        """
        return self._gid

    def home_subdir(self, subdir: str) -> str:
        """
        Returns the path to a subdirectory under the user's home directory on the host system.
        :param subdir: Subdirectory (e.g. ".ssh")
        :return: Absolute path to home sub
        """
        return os.path.join(self._home, subdir)

    @staticmethod
    def build() -> 'UnixUser':
        return UnixUser(
            os.environ['HOME'],
            os.environ['USER'],
            os.environ['XDG_RUNTIME_DIR'],
            os.getuid(),
            os.getgid()
        )
