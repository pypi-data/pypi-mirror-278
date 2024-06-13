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
from typing import ClassVar, Literal, Sequence

from babelwidget.main import backend_t
from babelwidget.main import base_h as library_wgt_h
from babelwidget.main import dropdown_choice_h as dropdown_choice_wgt_h
from babelwidget.main import text_line_h as text_line_wgt_h
from conf_ini_g.catalog.specification.annotation.collection import collection_t
from conf_ini_g.interface.window.parameter.value import value_wgt_a
from conf_ini_g.phase.specification.parameter.type import type_t

VALUE_FOR_NONE = ()

_DELIMITERS_TYPES = (tuple, list, set)
_DELIMITERS_VALUES = ("()", "[]", "{}")
_DELIMITERS = dict(zip(_DELIMITERS_TYPES, _DELIMITERS_VALUES))


@dtcl.dataclass(repr=False, eq=False)
class collection_wgt_t(value_wgt_a):
    """
    Cannot use slots (weak reference issue).
    """

    ENTRY_ANY: ClassVar[str] = "any"
    ENTRIES: ClassVar[tuple[str, ...]] = ("2", "3", "4", "5", "6", ENTRY_ANY)

    library_wgt: library_wgt_h
    backend: backend_t
    delimiters: Literal["()", "[]", "{}"] = dtcl.field(
        init=False, default=_DELIMITERS[tuple]
    )
    length_selector: dropdown_choice_wgt_h = dtcl.field(init=False, default=None)
    components: tuple[text_line_wgt_h, ...] = dtcl.field(init=False, default=None)

    @classmethod
    def NewForSpecification(
        cls,
        stripe: type_t | collection_t | None,
        backend: backend_t,
        /,
    ) -> collection_wgt_t:
        """
        If stripe does not contain the necessary details, a simple free-text input widget is used. If the value is not
        coherent with the details (which should not happen if stripe contains the necessary details and the value has
        been validated), a choice with the length of the value is added, with an exclamation point.
        """
        output = cls(library_wgt=backend.base_t(), backend=backend)

        output._SetUpComponents(stripe)
        for component in output.components:
            output.SetupValueChangedMessaging(component, "textChanged", backend)

        layout = backend.hbox_lyt_t()
        layout.setContentsMargins(0, 0, 0, 0)
        if output.length_selector is not None:
            layout.addWidget(output.length_selector)
        for component in output.components:
            layout.addWidget(component)
        output.library_wgt.setLayout(layout)

        return output

    def SetLength(self, new_index: int) -> None:
        """"""
        new_length = self.length_selector.ItemAt(new_index)
        if new_length == self.__class__.ENTRY_ANY:
            new_length = 1
        elif new_length.endswith("!"):
            new_length = int(new_length[:-1])
        else:
            new_length = int(new_length)
        _AdjustComponents(self.components, new_length)

    def _SetUpComponents(self, stripe: type_t | collection_t | None, /) -> None:
        """"""
        cls = self.__class__

        default_parameters = (cls.ENTRIES, int(cls.ENTRIES[-2]))
        if stripe is None:
            entries, max_entry = default_parameters
        else:
            if isinstance(stripe, type_t):
                annotation = stripe.FirstAnnotationWithType(collection_t)
            else:
                annotation = stripe
            if annotation is None:
                entries, max_entry = default_parameters
            elif (lengths := annotation.lengths) == collection_t.ANY_LENGTH:
                entries = (cls.ENTRY_ANY,)
                max_entry = None
            else:
                entries = tuple(str(_lgh) for _lgh in lengths)
                max_entry = lengths[-1]

        components = []
        if max_entry is None:
            if self.components is None:
                widget = self.backend.text_line_t(parent=None)
                components.append(widget)
        else:
            for e_idx in range(max_entry):
                if self.components is None:
                    widget = self.backend.text_line_t(parent=None)
                    components.append(widget)
        if self.components is None:
            self.components = tuple(components)

        if entries.__len__() > 1:
            if self.length_selector is None:
                length_selector = self.backend.dropdown_choice_t()
                for entry in entries:
                    length_selector.addItem(entry)
            else:
                length_selector = self.length_selector

            length_selector.setCurrentText(cls.ENTRY_ANY)

            if self.length_selector is None:
                self.length_selector = length_selector
                self.length_selector.SetFunction(self.SetLength)

    def Assign(
        self, value: tuple | None, stripe: type_t | collection_t | None, /
    ) -> None:
        """"""
        cls = self.__class__

        if value is None:
            value = VALUE_FOR_NONE

        delimiters = _DELIMITERS.get(type(value), None)
        if delimiters is None:
            raise TypeError(f"{type(value).__name__}: Unhandled sequence type.")

        self.delimiters = delimiters

        length = value.__len__()

        default_parameters = (cls.ENTRIES, int(cls.ENTRIES[-2]))
        if stripe is None:
            entries, max_entry = default_parameters
        else:
            if isinstance(stripe, type_t):
                annotation = stripe.FirstAnnotationWithType(collection_t)
            else:
                annotation = stripe
            if annotation is None:
                entries, max_entry = default_parameters
            elif (lengths := annotation.lengths) == collection_t.ANY_LENGTH:
                entries = (cls.ENTRY_ANY,)
                max_entry = None
            else:
                entries = tuple(str(_lgh) for _lgh in lengths)
                max_entry = lengths[-1]
                if (length > 0) and (str(length) not in entries):
                    # This should never happen since the value must have been validated
                    entries = entries + (str(length) + "!",)
                    max_entry = max(max_entry, length)

        components = []
        if max_entry is None:
            value_as_str = str(value)[1:-1] if length > 0 else ""
            if self.components is None:
                widget = self.backend.text_line_t(value_as_str)
                components.append(widget)
            else:
                self.components[0].setText(value_as_str)
        else:
            for e_idx in range(max_entry):
                value_as_str = str(value[e_idx]) if e_idx < length else ""
                if self.components is None:
                    widget = self.backend.text_line_t(value_as_str)
                    components.append(widget)
                else:
                    widget = self.components[e_idx]
                    widget.setText(value_as_str)
                if e_idx >= length:
                    widget.setVisible(False)
                    widget.setEnabled(False)
        if self.components is None:
            self.components = tuple(components)

        if entries.__len__() > 1:
            if self.length_selector is None:
                length_selector = self.backend.dropdown_choice_t()
                for entry in entries:
                    length_selector.addItem(entry)
            else:
                length_selector = self.length_selector

            if (length_as_str := str(length)) in entries:
                length_selector.setCurrentText(length_as_str)
            if length_as_str + "!" in entries:
                length_selector.setCurrentText(length_as_str + "!")
            else:  # cls.ENTRY_ANY is necessarily in entries
                length_selector.setCurrentText(cls.ENTRY_ANY)

            if self.length_selector is None:
                self.length_selector = length_selector
                self.length_selector.SetFunction(self.SetLength)

    def Text(self) -> str:
        """"""
        contents = []
        for component in self.components:
            # Do not use "visible" here since setting visible does not really set the property until it is actually
            # shown. The documentation explains about ancestors being visible or not, but it was not clear that the
            # property is apparently not effective immediately.
            if not component.isEnabled():
                break
            component_as_str = component.Text()
            if component_as_str == "":
                break
            contents.append(component_as_str)

        if contents.__len__() == 0:
            return self.delimiters
        elif contents.__len__() == 1:
            if self.delimiters[0] == "(":
                return f"({contents[0]},)"
            else:
                return f"[{contents[0]}]"
        else:
            return self.delimiters[0] + ", ".join(contents) + self.delimiters[1]


def _AdjustComponents(
    components: Sequence[text_line_wgt_h, ...],
    length: int,
) -> None:
    """"""
    for c_idx, component in enumerate(components):
        if c_idx < length:
            component.setVisible(True)
            component.setEnabled(True)
        else:
            component.setVisible(False)
            component.setEnabled(False)
