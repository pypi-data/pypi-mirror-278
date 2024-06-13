# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2023)
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

import types as t
import typing as h


def EventLoopClass(base_t: type, execute: str | h.Callable[[h.Any], int], /) -> type:
    """"""

    def _Run(self) -> int:
        """"""
        Execute = getattr(self, execute)
        return Execute()

    output = type("event_loop_t", (base_t,), {})
    if isinstance(execute, str):
        output.Run = _Run
    else:
        output.Run = execute

    return output


def ColorFunction(module: t.ModuleType, /) -> h.Callable[[str], h.Any]:
    """"""

    def _Color(name: str, /) -> module.QColorConstants:
        """"""
        return getattr(module.QColorConstants, name)

    return _Color


def ShowMessageFunction(
    module: t.ModuleType, execute: str, /
) -> h.Callable[[...], None]:
    """"""

    def _ShowMessage(title: str, message: str, /, *, parent=None) -> None:
        """"""
        dialog = module.QMessageBox(parent=parent)
        dialog.setWindowTitle(title)
        dialog.setText("<b>" + title + "</b>")
        dialog.setInformativeText(message)
        dialog.setStandardButtons(module.QMessageBox.StandardButton.Close)
        dialog.setDefaultButton(module.QMessageBox.StandardButton.Close)
        Execute = getattr(dialog, execute)
        Execute()

    return _ShowMessage


def ShowErrorMessageFunction(module: t.ModuleType, /) -> h.Callable[[...], None]:
    """"""

    def _ShowErrorMessage(message: str, /, *, parent=None) -> None:
        """"""
        module.QMessageBox.critical(parent, "Error", message)

    return _ShowErrorMessage
