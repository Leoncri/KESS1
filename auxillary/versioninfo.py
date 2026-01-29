class VersionInfo:
    def __init__(self, version: int, subversion: int) -> None:
        """
        Stores the version and the subversion of PGS Grideditor.

        Args:
            version (int): Positive integer represeting version of Grideditor
            subversion (int): Positive integer representing subversion of
                              Grideditor
        """
        if version < 0:
            raise ValueError("Version must be a positive integer.")
        if subversion < 0:
            raise ValueError("Subversion must be a positive integer.")
        self.version = version
        self.subversion = subversion