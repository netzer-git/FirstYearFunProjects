class UserNameException(Exception):
    """ User name is already taken """
    pass


class BookNameException(Exception):
    """ Book name is already taken """
    pass


class ReadingParameterException(Exception):
    """Invalid reading parameters"""
    pass
