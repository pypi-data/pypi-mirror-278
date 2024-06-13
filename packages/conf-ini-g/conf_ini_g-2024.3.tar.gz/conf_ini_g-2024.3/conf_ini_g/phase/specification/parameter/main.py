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
import textwrap as text
from typing import Any

from conf_ini_g.extension.string import AlignedOnSeparator
from conf_ini_g.phase.specification.base import base_t
from conf_ini_g.phase.specification.parameter.type import ANY_TYPE, type_t
from conf_ini_g.phase.specification.parameter.value import MISSING_REQUIRED_VALUE
from issue_manager import ISSUE_MANAGER
from str_to_obj import CastValue
from str_to_obj.interface.console import NameValueTypeAsRichStr, TypeAsRichStr
from str_to_obj.type.hint import any_hint_h


@dtcl.dataclass(repr=False, eq=False)
class parameter_t(base_t):
    """
    type:
        At instantiation time:
            - any_hint_h, if passed
            - type_t (ANY_TYPE), if not.
        After __post_init__: type_t
    """

    type: any_hint_h | type_t = ANY_TYPE
    default: Any = MISSING_REQUIRED_VALUE

    def __post_init__(self) -> None:
        """"""
        if not isinstance(self.type, type_t):
            self.type = type_t.NewFromTypeHint(self.type)

        with ISSUE_MANAGER.AddedContextLevel(
            f'Specification of {type(self).__name__} "{self.name}"'
        ):
            if self.optional:
                if self.default is MISSING_REQUIRED_VALUE:
                    ISSUE_MANAGER.Add(
                        "Invalid default value",
                        actual=MISSING_REQUIRED_VALUE,
                        expected="an explicit value",
                    )
                else:
                    converted, issues = CastValue(self.default, self.type)
                    if issues.__len__() > 0:
                        issues = ", ".join(issues)
                        ISSUE_MANAGER.Add(f"Invalid default value: {issues}")
                    else:
                        self.default = converted
            else:
                if not self.basic:
                    ISSUE_MANAGER.Add("Parameter is not basic but not optional")
                if self.default is not MISSING_REQUIRED_VALUE:
                    ISSUE_MANAGER.Add(
                        "Mandatory parameter with an explicit default value"
                    )

    @property
    def optional(self) -> bool:
        """"""
        return self.default is not MISSING_REQUIRED_VALUE

    def __rich__(self) -> str:
        """"""
        output = [
            TypeAsRichStr(self),
            *text.indent(super().__rich__(), "    ").splitlines(),
            f"    [blue]Template[/]@=@{self.type.__rich__()}",
            f"    {NameValueTypeAsRichStr('Default', self.default, separator='@=@')}",
            f"    [blue]Optional[/]@=@{self.optional}",
        ]

        output = AlignedOnSeparator(output, "@=@", " = ")

        return "\n".join(output)
