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
from typing import Annotated, ClassVar, Literal, Sequence

from conf_ini_g.catalog.specification.annotation.choices import choices_t
from str_to_obj import annotation_t
from str_to_obj.type.hint import annotated_hint_t


@dtcl.dataclass(slots=True, repr=False, eq=False)
class callable_t(annotation_t):
    ACCEPTED_TYPES = (str,)
    DUMMY_ENTRY: ClassVar[str] = "Dummy entry"
    SEPARATOR: ClassVar[str] = ":"
    kind: Literal["class", "function"]
    choices: choices_t | None = None
    allow_external: bool = False

    @classmethod
    def NewAnnotatedType(
        cls,
        /,
        *,
        kind: Literal["class", "function"] = "function",
        catalog: Sequence[str] | bool | None = None,
        allow_external: bool = False,
    ) -> annotated_hint_t:
        """"""
        if catalog is None:
            annotation = cls(kind=kind, allow_external=allow_external)
        elif isinstance(catalog, bool):
            if catalog:
                annotation = cls(
                    kind=kind,
                    choices=choices_t((cls.DUMMY_ENTRY,)),
                    allow_external=allow_external,
                )
            else:
                annotation = cls(kind=kind, allow_external=allow_external)
        else:
            annotation = cls(
                kind=kind, choices=choices_t(catalog), allow_external=allow_external
            )

        return Annotated[str, annotation]
