"""File manager exceptions"""


class NoFile(Exception):
    """No file exception"""

    ...


class ItemStructureAlredyExists(ValueError):
    """Item structure alredy exists"""

    def __init__(self, *args: object) -> None:
        super().__init__("Item structure already exists.", *args)
