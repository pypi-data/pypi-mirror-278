# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl
import string as strg

from issue_manager import ISSUE_MANAGER
from rich.text import Text as text_t

# Must not be <space> to allow assignment through command-line arguments.
_WORD_SEPARATOR = "_"
_VALID_CHARACTERS = strg.ascii_letters + strg.digits + _WORD_SEPARATOR


@dtcl.dataclass(repr=False, eq=False)  # Do not use slots here, only on last class.
class base_t:
    name: str
    definition: str = "No Definition Provided"
    description: str = "No Description Provided"
    basic: bool = True

    def __post_init__(self) -> None:
        """"""
        with ISSUE_MANAGER.AddedContextLevel(
            f'Specification of {type(self).__name__} "{self.name}"'
        ):
            if any(_chr not in _VALID_CHARACTERS for _chr in self.name):
                ISSUE_MANAGER.Add(
                    "Name contains invalid characters",
                    actual=self.name,
                    expected=f"name with characters from: {_VALID_CHARACTERS}",
                )
            if not isinstance(self.definition, str):
                ISSUE_MANAGER.Add(
                    f"Invalid type of definition",
                    actual=type(self.definition).__name__,
                    expected="str",
                )
            if not isinstance(self.description, str):
                ISSUE_MANAGER.Add(
                    f"Invalid type of description",
                    actual=type(self.description).__name__,
                    expected="str",
                )

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        return f"[blue]Name[/]@=@{self.name}\n[blue]Basic[/]@=@{self.basic}"
