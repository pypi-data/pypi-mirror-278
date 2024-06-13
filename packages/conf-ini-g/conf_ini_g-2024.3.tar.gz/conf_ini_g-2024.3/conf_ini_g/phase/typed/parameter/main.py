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

from typing import Any

from conf_ini_g.phase.specification.parameter.type import type_t
from conf_ini_g.phase.typed.parameter.invalid import INVALID_VALUE, invalid_value_t
from conf_ini_g.phase.typed.parameter.unit import ConvertedValue


def TypedValue(
    value: str,
    expected_type: type_t,
    /,
    *,
    unit: str | None = None,
    units: dict[str, int | float | invalid_value_t] = None,
) -> tuple[Any, list[str]]:
    """
    With unit consumed or not.
    """
    final_value, issues = expected_type.InterpretedValueOf(value)
    if issues.__len__() > 0:
        return INVALID_VALUE, [f"{value}: Invalid value: {', '.join(issues)}"]

    if (units is None) or (unit is None):
        return final_value, []

    conversion_factor = units.get(unit, None)
    if conversion_factor is None:
        return INVALID_VALUE, [f"{unit}: Missing unit definition."]
    if conversion_factor is INVALID_VALUE:
        return INVALID_VALUE, [f"{unit}: Invalid unit value."]

    converted, unconverted = ConvertedValue(final_value, conversion_factor)
    if unconverted.__len__() > 0:
        unconverted = ", ".join(unconverted)
        return INVALID_VALUE, [
            f"{unconverted}: Value(s) do(es) not support unit conversion."
        ]

    return converted, []
