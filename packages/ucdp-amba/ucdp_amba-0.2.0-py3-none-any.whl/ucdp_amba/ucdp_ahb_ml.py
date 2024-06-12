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
Unified Chip Design Platform - AMBA - AHB Multilayer.
"""

from collections import defaultdict
from logging import getLogger
from typing import ClassVar

import ucdp as u
from tabulate import tabulate
from ucdp_glbl import AddrSlave
from ucdp_glbl.addrdecoder import AddrDecoder

from . import types as t

LOGGER = getLogger(__name__)


class Master(u.NamedObject):
    """
    Master.
    """

    proto: t.AmbaProto
    """Protocol Version."""


class Slave(AddrSlave):
    """
    Slave.
    """

    proto: t.AmbaProto
    """Protocol Version."""


class UcdpAhbMlMod(u.ATailoredMod, AddrDecoder):
    """
    AHB Multilayer.

    Multilayer.
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
    """Default Protocol."""
    is_sub: bool = False
    """Full Address Decoding By Default."""

    masters: u.Namespace = u.Field(default_factory=u.Namespace)
    """Masters."""

    _master_slaves = u.PrivateField(default_factory=lambda: defaultdict(set))
    _slave_masters = u.PrivateField(default_factory=lambda: defaultdict(set))

    def _build(self):
        self.add_port(u.ClkRstAnType(), "main_i")

    def add_master(
        self,
        name: str,
        slavenames: u.Names | None = None,
        proto: t.AmbaProto | None = None,
        route: u.Routeable | None = None,
    ) -> Master:
        """
        Add master port named `name` connected to `route`.

        Args:
            name: Name or Pattern ('*' is supported)

        Keyword Args:
            slavenames: Names of slaves to be accessed by this master.
            proto: Protocol.
            route: port to connect this master to.
        """
        self.check_lock()
        proto = proto or self.proto
        master = Master(name=name, proto=proto)
        self.masters.add(master)

        self.add_interconnects((name,), slavenames)

        portname = f"ahb_mst_{name}_i"
        title = f"AHB Input {name!r}"
        self.add_port(t.AhbMstType(proto=proto), portname, title=title, comment=title)
        if route:
            self.con(portname, route)

        return master

    def add_slave(
        self,
        name: str,
        subbaseaddr=u.AUTO,
        size: u.Bytes | None = None,
        proto: t.AmbaProto | None = None,
        masternames: u.Names | None = None,
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
            masternames: Names of masters to be accessed by this slave.
            route: APB Slave Port to connect.
            ref: Logical Module connected.
        """
        self.check_lock()
        proto = proto or self.proto
        slave = Slave(name=name, addrdecoder=self, proto=proto, ref=ref)
        self.slaves.add(slave)
        if subbaseaddr is not None and (size is not None or self.default_size):
            slave.add_addrrange(subbaseaddr, size)

        self.add_interconnects(masternames, (name,))

        portname = f"ahb_slv_{name}_o"
        title = f"AHB Output {name!r}"
        self.add_port(t.AhbSlvType(proto=proto), portname, title=title, comment=title)
        if route:
            self.con(portname, route)

        return slave

    def add_interconnects(self, masternames: u.Names, slavenames: u.Names):
        """Add Interconnects."""
        self.check_lock()
        for mastername in u.split(masternames):
            for slavename in u.split(slavenames):
                self._master_slaves[mastername].add(slavename)
                self._slave_masters[slavename].add(mastername)

    @property
    def master_slaves(self) -> tuple[tuple[Master, tuple[Slave, ...]], ...]:
        """Masters and Their Slaves."""
        pairs: list[tuple[Master, tuple[Slave, ...]]] = []
        for master in self.masters:
            slavenames = self._master_slaves[master.name]
            slaves = tuple(self.slaves[slavename] for slavename in slavenames)
            pairs.append((master, slaves))
        return tuple(pairs)

    @property
    def slave_masters(self) -> tuple[tuple[Slave, tuple[Master, ...]], ...]:
        """Slaves and Their Masters."""
        pairs: list[tuple[Slave, tuple[Master, ...]]] = []
        for slave in self.slaves:
            masternames = self._slave_masters[slave.name]
            masters = tuple(self.masters[mastername] for mastername in masternames)
            pairs.append((slave, masters))
        return tuple(pairs)

    def _builddep(self):
        # Basic checks
        masters = self.masters
        slaves = self.slaves
        if not masters:
            LOGGER.warning("%s has not masters", self)
        if not slaves:
            LOGGER.warning("%s has not slaves", self)
        for master, slaves in self.master_slaves:
            if not slaves:
                LOGGER.warning("%s: %r has not slaves", self, master)
        for slave, masters in self.slave_masters:
            if not masters:
                LOGGER.warning("%s: %r has not masters", self, slave)

    def get_overview(self):
        """Return overview tables."""
        overview = [
            f"Protocol: {self.proto}",
            self._get_overview_matrix(),
            self.addrmap.get_overview(),
        ]
        return "\n\n\n".join(overview)

    def _get_overview_matrix(self) -> str:
        slaves = self.slaves
        headers = ["Master > Slave"] + [slave.name for slave in slaves]
        idxmap = {slave.name: idx for idx, slave in enumerate(slaves, 1)}
        empty = ["" for slave in slaves]
        matrix = []
        for master, slaves in self.master_slaves:
            item = [master.name, *empty]
            for slave in slaves:
                item[idxmap[slave.name]] = "X"
            matrix.append(item)
        return tabulate(matrix, headers=headers, stralign="center")

    @staticmethod
    def build_top(**kwargs):
        """Build example top module and return it."""
        return UcdpAhbMlExampleMod()


class UcdpAhbMlExampleMod(u.AMod):
    """Just an Example Multilayer."""

    def _build(self):
        ml = UcdpAhbMlMod(self, "u_ml")
        ml.add_master("ext")
        ml.add_master("dsp")

        slv = ml.add_slave("ram", masternames=["ext", "dsp"])
        slv.add_addrrange(0xF0000000, size=2**16)

        slv = ml.add_slave("periph")
        slv.add_addrrange(0xF0010000, size="64kb")

        slv = ml.add_slave("misc")
        slv.add_addrrange(size="32k")

        # slv = ml.add_slave("ext", masternames=["ext", "dsp"])
        # slv.add_addrrange(0x0, size=2**32)
        # slv.add_exclude_addrrange(0xF0000000, size=2**18)

        ml.add_interconnects("dsp", "periph")
        ml.add_interconnects("external", "misc")
