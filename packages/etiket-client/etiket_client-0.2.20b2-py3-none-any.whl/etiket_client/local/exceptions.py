# scope exceptions
class ScopeDoesAlreadyExistException(Exception):
    pass
class ScopeDoesNotExistException(Exception):
    pass
class CannotDeleteAScopeWithDatasetsException(Exception):
    pass
class MemberHasNoBusinessInThisScopeException(Exception):
    pass
class UserAlreadyNotPartOfScopeException(Exception):
    pass
class UserAlreadyPartOfScopeException(Exception):
    pass
class SchemaAlreadyAssignedException(Exception):
    pass

# user exceptions
class UserAlreadyExistsException(Exception):
    pass
class UserMailAlreadyRegisteredException(Exception):
    pass
class UserDoesNotExistException(Exception):
    pass

# schema exceptions
class SchemaDoesNotExistException(Exception):
    pass
class SchemaDoesAlreadyExistException(Exception):
    pass

# dataset exceptions
class  DatasetAlreadyExistException(Exception):
    pass
class DatasetAltUIDAlreadyExistException(Exception):
    pass
class DatasetNotFoundException(Exception):
    pass

class MultipleDatasetFoundException(Exception):
    pass

class DatasetFoundInMultipleScopesException(Exception):
    pass

# files exceptions
class FileNotAvailableException(Exception):
    pass
class FileAlreadyExistsException(Exception):
    pass
class UnexpectedFileVersionException(Exception):
    pass