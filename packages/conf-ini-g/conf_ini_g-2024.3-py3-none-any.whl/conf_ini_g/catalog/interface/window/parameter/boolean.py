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

from __future__ import annotations

import dataclasses as dtcl
from typing import Any

from babelwidget.main import backend_t
from babelwidget.main import base_h as library_wgt_h
from babelwidget.main import radio_choice_h as radio_choice_wgt_h
from conf_ini_g.catalog.specification.annotation.boolean import boolean_t
from conf_ini_g.interface.window.parameter.value import value_wgt_a
from conf_ini_g.phase.specification.parameter.type import type_t


@dtcl.dataclass(repr=False, eq=False)
class boolean_wgt_t(value_wgt_a):
    library_wgt: library_wgt_h
    true_btn: radio_choice_wgt_h | None = dtcl.field(init=False, default=None)
    false_btn: radio_choice_wgt_h | None = dtcl.field(init=False, default=None)

    @classmethod
    def NewForSpecification(
        cls,
        stripe: type_t | boolean_t | None,
        backend: backend_t,
        /,
    ) -> boolean_wgt_t:
        """"""
        output = cls(library_wgt=backend.base_t())

        if stripe is None:
            annotation = None
        elif isinstance(stripe, type_t):
            annotation = stripe.FirstAnnotationWithType(boolean_t)
        else:
            annotation = stripe
        if annotation is None:
            labels = ("True", "False")
        else:
            labels = getattr(annotation.mode, "value", None)

        true_btn = backend.radio_choice_t(labels[0], parent=output.library_wgt)
        false_btn = backend.radio_choice_t(labels[1], parent=output.library_wgt)

        output.true_btn = true_btn
        output.false_btn = false_btn

        output.SetupValueChangedMessaging(output.true_btn, "released", backend)

        layout = backend.hbox_lyt_t()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(true_btn)
        layout.addWidget(false_btn)
        output.library_wgt.setLayout(layout)

        return output

    def Assign(self, value: bool, _: Any, /) -> None:
        """"""
        self.true_btn.setChecked(value)
        self.false_btn.setChecked(not value)

    def Text(self) -> str:
        """"""
        return str(self.true_btn.isChecked())
