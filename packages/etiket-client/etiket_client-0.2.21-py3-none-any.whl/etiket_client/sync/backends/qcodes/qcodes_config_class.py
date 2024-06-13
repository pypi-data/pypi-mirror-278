import pathlib, dataclasses

@dataclasses.dataclass
class QCoDeSConfigData:
    database_directory: pathlib.Path
    set_up : str