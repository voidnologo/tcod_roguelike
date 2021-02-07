class Impossible(Exception):
    """
    Action is impossible to perform
    Reason in the exception message
    """

    pass


class QuitWithoutSaving(SystemExit):
    """
    Can be raised to exit the game without automatically saving.
    """

    pass
