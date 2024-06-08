class DuplicateBlockIdError(Exception):
    """Error indicating that duplicate ids were present on blocks within a Canvas."""

    pass


class NoMatchingBlocksError(Exception):
    """
    Error indicating that blocks were expected, but none matched.

    Used to prevent requiring developers to handle Optional[_UiBlock] for type safety.
    """

    pass
