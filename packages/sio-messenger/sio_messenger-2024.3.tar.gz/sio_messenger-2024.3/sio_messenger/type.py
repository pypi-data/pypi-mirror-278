# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2024)
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

import collections.abc as i
import typing as h
from enum import Enum as enum_t

source_h = h.Any
# i.Hashable: a hashable source, or an str built from a non-hashable source.
educated_source_h = i.Hashable
canal_name_h = str | enum_t
canal_h = canal_name_h | tuple[educated_source_h, canal_name_h]
receiver_action_h = h.Callable[[...], None] | h.Callable[[source_h, ...], None]


class CanalNotFoundError(Exception):
    pass


class CanalOrActionNotFoundError(Exception):
    pass


class ExistingActionError(Exception):
    pass


class MissingSourceError(Exception):
    pass


class messenger_t(dict[canal_h, list[receiver_action_h]]):
    """
    Canal: From (known or unknown) source, and specialized by a message type (its name),
    to message acknowledgement function.
    Limitation: the name "source" cannot be a kwarg of receiver actions.
    """

    _actions_needing_source: set[receiver_action_h]

    def __init__(self) -> None:
        """"""
        dict.__init__(self)
        self._actions_needing_source = set()

    def AddCanal(
        self,
        name: canal_name_h,
        MessageReceiverAction: receiver_action_h,
        /,
        *,
        source: source_h | None = None,
        action_needs_source: bool = False,
    ) -> None:
        """"""
        canal = _CanalFromSourceAndName(source, name)

        if canal not in self:
            self[canal] = []

        if MessageReceiverAction in self[canal]:
            raise ExistingActionError(
                f"Message receiver action {MessageReceiverAction.__name__} "
                f"already exists for canal {canal}."
            )

        self[canal].append(MessageReceiverAction)
        if action_needs_source:
            if source is None:
                raise MissingSourceError(
                    f"No source passed for canal {canal} and "
                    f"receiver action {MessageReceiverAction.__name__}."
                )
            self._actions_needing_source.add(MessageReceiverAction)

    def RemoveReceiverAction(
        self,
        MessageReceiverAction: receiver_action_h,
        /,
        *,
        name: canal_name_h | None = None,
        source: source_h | None = None,
    ) -> None:
        """"""
        if name is None:
            for actions in self.values():
                if MessageReceiverAction in actions:
                    actions.remove(MessageReceiverAction)

            if MessageReceiverAction in self._actions_needing_source:
                self._actions_needing_source.remove(MessageReceiverAction)
            return

        canal = _CanalFromSourceAndName(source, name)

        if (canal in self) and (MessageReceiverAction in self[canal]):
            self[canal].remove(MessageReceiverAction)
            if self[canal].__len__() == 0:
                del self[canal]

            if MessageReceiverAction in self._actions_needing_source:
                self._actions_needing_source.remove(MessageReceiverAction)
        else:
            raise CanalOrActionNotFoundError(
                f"Canal {canal} or message receiver action "
                f"{MessageReceiverAction.__name__} not found."
            )

    def RemoveCanal(
        self, name: canal_name_h, /, *, source: source_h | None = None
    ) -> None:
        """"""
        canal = _CanalFromSourceAndName(source, name)

        if canal in self:
            # Here, the cleaning of self._actions_needing_source is not done...
            # Maybe one day.
            del self[canal]
        else:
            raise CanalNotFoundError(f"Canal {canal} not found.")

    def Transmit(
        self,
        name: canal_name_h,
        /,
        *args,
        source: source_h | None = None,
        **kwargs,
    ) -> None:
        """"""
        canal = _CanalFromSourceAndName(source, name)

        if canal in self:
            for MessageReceiverAction in self[canal]:
                if MessageReceiverAction in self._actions_needing_source:
                    MessageReceiverAction(source, *args, **kwargs)
                else:
                    MessageReceiverAction(*args, **kwargs)
        else:
            raise CanalNotFoundError(f"Canal {canal} not found.")


def _CanalFromSourceAndName(source: source_h | None, name: canal_name_h, /) -> canal_h:
    """"""
    if source is None:
        return name

    if not isinstance(source, i.Hashable):
        # Hopefully, this can serve as a unique id (actually, id(source) alone should
        # work).
        source = f"{type(source).__name__}.{id(source)}"

    return source, name
