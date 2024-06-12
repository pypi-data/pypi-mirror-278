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
Unified Chip Design Platform - AMBA - AHB2APB.
"""

from logging import getLogger
from typing import ClassVar

import ucdp as u
from ucdp_glbl import AddrDecoder, AddrSlave
from ucdp_glbl.types import LevelIrqType

from . import types as t

LOGGER = getLogger(__name__)


class Slave(AddrSlave):
    """
    Slave.
    """

    proto: t.AmbaProto
    """Protocol Version."""


class UcdpAhb2apbMod(u.ATailoredMod, AddrDecoder):
    """
    AHB to APB Bridge.

    >>> class Mod(u.AMod):
    ...     def _build(self):
    ...         ahb2apb = UcdpAhb2apbMod(self, "u_ahb2apb")
    ...         ahb2apb.add_slave("uart")
    ...         ahb2apb.add_slave("spi")

    >>> ahb2apb = Mod().get_inst("u_ahb2apb")
    >>> print(ahb2apb.get_overview())
    Size: 8 KB
    <BLANKLINE>
    | Addrspace | Type  | Base    | Size           | Attributes |
    | --------- | ----  | ----    | ----           | ---------- |
    | uart      | Slave | +0x0    | 1024x32 (4 KB) | Sub        |
    | spi       | Slave | +0x1000 | 1024x32 (4 KB) | Sub        |
    <BLANKLINE>
    """

    filelists: ClassVar[u.ModFileLists] = (
        u.ModFileList(
            name="hdl",
            gen="full",
            filepaths=("$PRJROOT/{mod.topmodname}/{mod.modname}.sv"),
            template_filepaths=("ucdp_ahb2apb.sv.mako", "sv.mako"),
        ),
    )

    proto: t.AmbaProto = t.AmbaProto()
    errirq: bool = False
    is_sub: bool = True
    default_size: u.Bytes | None = 4096

    def _build(self):
        self.add_port(u.ClkRstAnType(), "main_i")

        if self.errirq:
            title = "APB Error Interrupt"
            self.add_port(LevelIrqType(), "irq_o", title=title, comment=title)

        self.add_port(t.AhbSlvType(proto=self.proto), "ahb_slv_i")

    def add_slave(
        self,
        name: str,
        subbaseaddr=u.AUTO,
        size: u.Bytes | None = None,
        proto: t.AmbaProto | None = None,
        route: u.Routeable | None = None,
        ref: u.BaseMod | str | None = None,
    ):
        """
        Add APB Slave.

        Args:
            name: Slave Name.

        Keyword Args:
            subbaseaddr: Base address, Next Free address by default. Do not add address space if `None`.
            size: Address Space.
            proto: AMBA Protocol Selection.
            route: APB Slave Port to connect.
            ref: Logical Module connected.
            auser: User vector if there is not incoming `auser` signal.
        """
        proto = proto or self.proto
        slave = Slave(name=name, addrdecoder=self, proto=proto, ref=ref)
        self.slaves.add(slave)
        if subbaseaddr is not None and (size is not None or self.default_size):
            slave.add_addrrange(subbaseaddr, size)

        portname = f"apb_slv_{name}_o"
        title = f"APB Slave {name!r}"
        self.add_port(t.ApbSlvType(proto=proto), portname, title=title, comment=title)
        if route:
            self.con(portname, route)

        return slave

    def _builddep(self):
        if not self.slaves:
            LOGGER.error("%r: has no APB slaves", self)

    def get_overview(self):
        """Overview."""
        return self.addrmap.get_overview(skip_words_fields=True)

    @staticmethod
    def build_top(**kwargs):
        """Build example top module and return it."""
        return UcdpAhb2apbExampleMod()


class UcdpAhb2apbExampleMod(u.AMod):
    """
    Just an Example.
    """

    def _build(self):
        class SecIdType(t.ASecIdType):
            def _build(self):
                self._add(0, "apps")
                self._add(2, "comm")
                self._add(5, "audio")

        amba5 = t.AmbaProto(name="amba5", secidtype=SecIdType(default=2))

        for errirq in (False, True):
            for proto in (t.AMBA3, amba5):
                name = f"u_ahb2apb_{proto.name}_errirq{errirq}".lower()
                ahb2apb = UcdpAhb2apbMod(self, name, proto=proto, errirq=errirq)
                ahb2apb.add_slave("default")
                ahb2apb.add_slave("slv3", proto=t.AMBA3)
                ahb2apb.add_slave("slv5", proto=amba5)

        ahb2apb = UcdpAhb2apbMod(self, "u_odd")
        ahb2apb.add_slave("foo")
        slv = ahb2apb.add_slave("bar")
        ahb2apb.add_slave("baz", size="13kB")
        slv.add_addrrange()
