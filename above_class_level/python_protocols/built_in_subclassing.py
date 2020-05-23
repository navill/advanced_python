from collections import UserDict
from typing import Any, Hashable


class DistinctError(ValueError):
    """Raised when duplicate value is added to a distinctdict."""


class distinctdict(UserDict):
    """Dictionary that does not accept duplicate values."""

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if value in self.values():
            if (key in self and self[key] != value) or (key not in self):
                raise DistinctError(
                    "This value already exists for different key"
                )

        super().__setitem__(key, value)


user_dict = distinctdict()
user_dict['a'] = 1
user_dict['b'] = 2
user_dict['c'] = 3
print(user_dict)
# user_dict['d'] = 1  # raise error

from collections import UserList


class Folder(UserList):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def dir(self, nesting: int = 0) -> None:
        offset = "  " * nesting
        # print root folder
        print('%s%s/' % (offset, self.name))

        for element in self:
            if hasattr(element, 'dir'):
                # print nested folder
                element.dir(nesting + 1)
            else:
                # print file
                print("%s  %s" % (offset, element))


tree = Folder('project')
tree.append('README.md')

src = Folder('src')
src.append('script.py')
tree.append(src)
tree.dir()
# project/
#   README.md
#   src/
#     script.py
tree.remove(src)
tree.dir()
# project/
#   README.md
