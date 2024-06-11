#
# MIT License
#
# Copyright (c) 2024 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Generic Slave.
"""

import ucdp as u
from icdutil import num
from ucdp_glbl.addrspace import Addrspace

from . import types as t
from .demux import Demux

NOMOD = u.Object()


class Slave(u.NamedObject):
    """
    Slave.
    """

    demux: Demux = u.Field(repr=False)
    """Demultiplexer Addressing This Slave."""

    proto: t.AmbaProto
    """Protocol Version."""

    mod: u.BaseMod | str | None
    """Addressed Module."""

    def add_addrrange(self, subbaseaddr=u.AUTO, size: u.Bytes | None = None) -> "SlaveAddrspace":
        """
        Add Address Range.

        Keyword Args:
            subbaseaddr: Sub Start Address. Take next free if 'AUTO'.
            size: Address Range Size (i.e. '4k')
            mod: Reference module or path to it.
        """
        demux = self.demux
        addrmap = demux.addrmap

        # size
        if size is None:
            size = demux.default_size
        else:
            size = u.Bytes(size)

        # subbaseaddr
        if size is not None:
            align = num.calc_next_power_of(size)
            if subbaseaddr is u.AUTO:
                subbaseaddr = addrmap.get_free_baseaddr(align)
            if subbaseaddr != num.align(subbaseaddr, align=align):
                raise ValueError(f"subbaseaddr {subbaseaddr!r} is not aligned to {align!r}")

        addrspace = SlaveAddrspace(name=self.name, baseaddr=subbaseaddr, size=size, slave=self, is_sub=demux.is_sub)
        addrmap.add(addrspace)
        return addrspace


class SlaveAddrspace(Addrspace):
    """Slave Address Space."""

    slave: Slave
