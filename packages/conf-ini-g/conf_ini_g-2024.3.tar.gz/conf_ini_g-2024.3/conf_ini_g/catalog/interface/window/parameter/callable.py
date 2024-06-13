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
import inspect as nspt
import typing as h
from importlib import util as mprt
from pathlib import Path as pl_path_t

from babelwidget.main import backend_t
from babelwidget.main import base_h as library_wgt_h
from conf_ini_g.catalog.interface.window.parameter.choices import choices_wgt_t
from conf_ini_g.catalog.interface.window.parameter.path import path_wgt_t
from conf_ini_g.catalog.specification.annotation.callable import callable_t
from conf_ini_g.catalog.specification.annotation.path import path_t as path_annotation_t
from conf_ini_g.interface.window.parameter.value import value_wgt_a
from conf_ini_g.phase.specification.parameter.type import type_t


@dtcl.dataclass(repr=False, eq=False)
class callable_wgt_t(value_wgt_a):
    library_wgt: library_wgt_h
    backend: backend_t
    kind: h.Literal["class", "function"]
    path: path_wgt_t | None = dtcl.field(init=False, default=None)
    choices: choices_wgt_t = dtcl.field(init=False, default=None)

    @classmethod
    def NewForSpecification(
        cls,
        stripe: type_t | callable_t,
        backend: backend_t,
        /,
    ) -> callable_wgt_t:
        """"""
        if isinstance(stripe, type_t):
            annotation = stripe.FirstAnnotationWithType(callable_t)
            if annotation is None:
                raise ValueError("No catalog provided.")
        else:
            annotation = stripe
        kind = annotation.kind
        choices = annotation.choices
        allow_external = annotation.allow_external

        choices_wgt = choices_wgt_t.NewForSpecification(
            choices,
            backend,
        )

        if allow_external:
            output = cls(
                library_wgt=backend.base_t(),
                backend=backend,
                kind=kind,
            )
        else:
            output = cls(
                library_wgt=choices_wgt,
                backend=backend,
                kind=kind,
            )
        output.choices = choices_wgt

        # TODO: Check that this is the correct emitter and signal.
        output.SetupValueChangedMessaging(output.choices, "released", backend)

        if allow_external:
            path_wgt = path_wgt_t.NewForSpecification(
                path_annotation_t(
                    target_type=path_annotation_t.TARGET_TYPE.document, is_input=True
                ),
                backend,
                PostAssignmentFunction=output._UpdateChoices,
            )
            output.path = path_wgt

            layout = backend.hbox_lyt_t()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(path_wgt.library_wgt)
            layout.addWidget(choices_wgt.library_wgt)
            output.library_wgt.setLayout(layout)

        return output

    def _UpdateChoices(self, path: pl_path_t, /) -> None:
        """"""
        self.choices.library_wgt.clear()

        spec = mprt.spec_from_file_location(path.stem, path)
        module = spec.loader.load_module(spec.name)
        if self.kind == "class":
            condition = nspt.isclass
        else:
            condition = nspt.isfunction

        for name, _ in nspt.getmembers(module, condition):
            if not name.startswith("_"):
                self.choices.library_wgt.addItem(name)

    def SetFunction(self, function: h.Callable, /) -> None:
        """
        self.activated.connect(function): Responds only to GUI interaction, not
        programmatic change.
        """
        self.choices.currentIndexChanged.connect(function)

    def Assign(self, value: str, _: h.Any, /) -> None:
        """"""
        if callable_t.SEPARATOR in value:
            path, choice = value.split(callable_t.SEPARATOR)
            self.path.Assign(pl_path_t(path), None)
        else:
            choice = value
        self.choices.Assign(choice, None)

    def Text(self) -> str:
        """"""
        if self.path is None:
            return self.choices.Text()

        path = self.path.Text()
        if path.__len__() > 0:
            return f"{path}{callable_t.SEPARATOR}{self.choices.Text()}"

        return self.choices.Text()
