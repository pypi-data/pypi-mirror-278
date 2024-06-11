#
# MIT License
#
# Copyright (c) 2024 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, mowithcommentestriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and toublicommentistribute, sublicense, and/or sell
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

AMBA Type Definitions.

Mainly these types are needed:

* :any:`AhbMstType`
* :any:`AhbSlvType`
* :any:`ApbSlvType`
"""

import ucdp as u


class AuserType(u.UintType):
    """
    Address User Channel (AMBA5 Lite).
    """

    title: str = "Address User Channel"
    comment: str = "Address User Channel"

    def __init__(self, **kwargs):
        super().__init__(width=4, **kwargs)


class ASecIdType(u.AEnumType):
    """
    Base of all Security ID Types.
    """

    keytype: u.UintType = u.UintType(4)

    def get_subset_type(self, excludes: u.Names | None = None):
        """Return variant with element excluded."""
        excludes = u.split(excludes)
        return self.new(filter_=lambda item: item.value not in excludes)


class AmbaProto(u.AConfig):
    """Amba Protocol Version."""

    secidtype: ASecIdType | None = None

    @property
    def ausertype(self) -> AuserType | None:
        """Protocol has hauser signal."""
        if self.secidtype:
            return AuserType(default=self.calc_auser(secid=self.secidtype.default))
        return None

    def calc_auser(self, secname=None, secid=None):
        """Calculate AUSER signal."""
        value = 0
        secidtype = self.secidtype
        if self.secidtype:
            if secname:
                value = secidtype.encode(secname)
            elif secid is not None:
                value = secid
            else:
                value = secidtype.default
        return value


AMBA3 = AmbaProto(name="amba3")


class AhbMstType(u.AStructType):
    """
    From AHB Master.

    Keyword Args:
        proto (Protocol): Protocol feature set selection.

    The default type:

    >>> for item in AhbMstType().values(): item
    StructItem('htrans', AhbTransType(), doc=Doc(title='AHB Transfer Type', ...))
    StructItem('haddr', AhbAddrType(32), doc=Doc(title='AHB Bus Address', ...))
    StructItem('hwrite', AhbWriteType(), doc=Doc(title='AHB Write Enable', ...))
    StructItem('hsize', AhbSizeType(), doc=Doc(title='AHB Size', ...))
    StructItem('hburst', AhbBurstType(), doc=Doc(title='AHB Burst Type', ...))
    StructItem('hprot', AhbProtType(4), doc=Doc(title='AHB Transfer Protection', ...))
    StructItem('hwdata', AhbDataType(32), doc=Doc(title='AHB Data', ...))
    StructItem('hready', AhbReadyType(), orientation=BWD, doc=Doc(title='AHB Transfer Done', ...))
    StructItem('hresp', AhbRespType(), orientation=BWD, doc=Doc(title='AHB Response Error', ...))
    StructItem('hrdata', AhbDataType(32), orientation=BWD, doc=Doc(title='AHB Data', ...))

    With `hauser`:

    >>> class SecIdType(ASecIdType):
    ...     def _build(self):
    ...         self._add(0, "apps")
    ...         self._add(2, "comm")
    ...         self._add(5, "audio")
    >>> ahb5 = AmbaProto("AHB5", secidtype=SecIdType(default=2))

    >>> for item in AhbMstType(proto=ahb5).values(): item
    StructItem('htrans', AhbTransType(), doc=Doc(title='AHB Transfer Type', ...))
    StructItem('haddr', AhbAddrType(32), doc=Doc(title='AHB Bus Address', ...))
    StructItem('hwrite', AhbWriteType(), doc=Doc(title='AHB Write Enable', ...))
    StructItem('hsize', AhbSizeType(), doc=Doc(title='AHB Size', ...))
    StructItem('hburst', AhbBurstType(), doc=Doc(title='AHB Burst Type', ...))
    StructItem('hprot', AhbProtType(4), doc=Doc(title='AHB Transfer Protection', ...))
    StructItem('hwdata', AhbDataType(32), doc=Doc(title='AHB Data', ...))
    StructItem('hready', AhbReadyType(), orientation=BWD, doc=Doc(title='AHB Transfer Done', ...))
    StructItem('hresp', AhbRespType(), orientation=BWD, doc=Doc(title='AHB Response Error', ...))
    StructItem('hrdata', AhbDataType(32), orientation=BWD, doc=Doc(title='AHB Data', ...))

    Both protocol versions are not connectable:

    >>> AhbMstType().is_connectable(AhbMstType(proto=ahb5))
    False

    But casting is allowed:

    >>> for item in AhbMstType().cast(AhbMstType(proto=ahb5)): item
    ('', '')
    ('htrans', 'htrans')
    ('haddr', 'haddr')
    ('hwrite', 'hwrite')
    ('hsize', 'hsize')
    ('hburst', 'hburst')
    ('hprot', 'hprot')
    ('hwdata', 'hwdata')
    ('hready', 'hready')
    ('hresp', 'hresp')
    ('hrdata', 'hrdata')

    It is also not allowed to connect Master and Slave:

    >>> AhbMstType().is_connectable(AhbSlvType())
    False

    But casting is allowed in all ways.

    >>> len(tuple(AhbMstType().cast(AhbSlvType())))
    12
    >>> len(tuple(AhbMstType(proto=ahb5).cast(AhbSlvType())))
    11
    >>> len(tuple(AhbMstType(proto=ahb5).cast(AhbSlvType(proto=ahb5))))
    12
    """

    title: str = "AHB Master"
    comment: str = "AHB Master"
    proto: AmbaProto = AMBA3

    def _build(self):
        # FWD
        self._add("htrans", AhbTransType())
        self._add("haddr", AhbAddrType())
        ausertype = self.proto.ausertype
        if ausertype:
            self._add("hauser", ausertype, title="AHB Address User Channel")
        self._add("hwrite", AhbWriteType())
        self._add("hsize", AhbSizeType())
        self._add("hburst", AhbBurstType())
        self._add("hprot", AhbProtType())
        self._add("hwdata", AhbDataType())
        # BWD
        self._add("hready", AhbReadyType(), u.BWD)
        self._add("hresp", AhbRespType(), u.BWD)
        self._add("hrdata", AhbDataType(), u.BWD)

    def cast(self, other):
        """
        How to cast an assign of type `self` from a value of type `other`.

        `self = cast(other)`
        """
        if isinstance(other, AhbMstType) and self.proto != other.proto:
            # Drive a Mst with Mst signals
            yield "", ""
            yield "htrans", "htrans"
            yield "haddr", "haddr"
            # never use hauser
            yield "hwrite", "hwrite"
            yield "hsize", "hsize"
            yield "hburst", "hburst"
            yield "hprot", "hprot"
            yield "hwdata", "hwdata"
            # BWD
            yield "hready", "hready"
            yield "hresp", "hresp"
            yield "hrdata", "hrdata"
        elif isinstance(other, AhbSlvType):
            # Drive a Mst with Slv signals
            yield "", ""
            yield "htrans", "htrans"
            yield "haddr", "haddr"
            if self.proto.ausertype == other.proto.ausertype:
                yield "hauser", "hauser"
            yield "hwrite", "hwrite"
            yield "hsize", "hsize"
            yield "hburst", "hburst"
            yield "hprot", "hprot"
            yield "hwdata", "hwdata"
            # BWD
            yield "hready", "hreadyout"
            # yield "hready", "hready" TODO: @djakschik, extend cast support
            yield "hresp", "hresp"
            yield "hrdata", "hrdata"
        else:
            return None


class AhbSlvType(u.AStructType):
    """
    To AHB Slave.

    Keyword Args:
        proto (Protocol): Protocol feature set selection.

    The default type:

    >>> for item in AhbSlvType().values(): item
    StructItem('hsel', AhbSelType(), doc=Doc(title='AHB Slave Select', ...))
    StructItem('haddr', AhbAddrType(32), doc=Doc(title='AHB Bus Address', ...))
    StructItem('hwrite', AhbWriteType(), doc=Doc(title='AHB Write Enable', ...))
    StructItem('htrans', AhbTransType(), doc=Doc(title='AHB Transfer Type', ...))
    StructItem('hsize', AhbSizeType(), doc=Doc(title='AHB Size', ...))
    StructItem('hburst', AhbBurstType(), doc=Doc(title='AHB Burst Type', ...))
    StructItem('hprot', AhbProtType(4), doc=Doc(title='AHB Transfer Protection', ...))
    StructItem('hwdata', AhbDataType(32), doc=Doc(title='AHB Data', ...))
    StructItem('hready', AhbReadyType(), doc=Doc(title='AHB Transfer Done to Slave', ...))
    StructItem('hreadyout', AhbReadyType(), orientation=BWD, doc=Doc(title='AHB Transfer Done from Slave', ...))
    StructItem('hresp', AhbRespType(), orientation=BWD, doc=Doc(title='AHB Response Error', ...))
    StructItem('hrdata', AhbDataType(32), orientation=BWD, doc=Doc(title='AHB Data', ...))

    With `hauser`:

    >>> class SecIdType(ASecIdType):
    ...     def _build(self):
    ...         self._add(0, "apps")
    ...         self._add(2, "comm")
    ...         self._add(5, "audio")
    >>> ahb5 = AmbaProto("AHB5", secidtype=SecIdType(default=2))

    >>> for item in AhbSlvType(proto=ahb5).values(): item
    StructItem('hsel', AhbSelType(), doc=Doc(title='AHB Slave Select', ...))
    StructItem('haddr', AhbAddrType(32), doc=Doc(title='AHB Bus Address', ...))
    StructItem('hwrite', AhbWriteType(), doc=Doc(title='AHB Write Enable', ...))
    StructItem('htrans', AhbTransType(), doc=Doc(title='AHB Transfer Type', ...))
    StructItem('hsize', AhbSizeType(), doc=Doc(title='AHB Size', ...))
    StructItem('hburst', AhbBurstType(), doc=Doc(title='AHB Burst Type', ...))
    StructItem('hprot', AhbProtType(4), doc=Doc(title='AHB Transfer Protection', ...))
    StructItem('hwdata', AhbDataType(32), doc=Doc(title='AHB Data', ...))
    StructItem('hready', AhbReadyType(), doc=Doc(title='AHB Transfer Done to Slave', ...))
    StructItem('hreadyout', AhbReadyType(), orientation=BWD, doc=Doc(title='AHB Transfer Done from Slave', ...))
    StructItem('hresp', AhbRespType(), orientation=BWD, doc=Doc(title='AHB Response Error', ...))
    StructItem('hrdata', AhbDataType(32), orientation=BWD, doc=Doc(title='AHB Data', ...))

    Both protocol versions are not connectable:

    >>> AhbSlvType().is_connectable(AhbSlvType(proto=ahb5))
    False

    But casting is allowed:

    >>> for item in AhbSlvType().cast(AhbSlvType(proto=ahb5)): item
    ('', '')
    ('hsel', 'hsel')
    ('haddr', 'haddr')
    ('hwrite', 'hwrite')
    ('htrans', 'htrans')
    ('hsize', 'hsize')
    ('hburst', 'hburst')
    ('hprot', 'hprot')
    ('hwdata', 'hwdata')
    ('hready', 'hready')
    ('hreadyout', 'hreadyout')
    ('hresp', 'hresp')
    ('hrdata', 'hrdata')

    It is also not allowed to connect Master and Slave:

    >>> AhbSlvType().is_connectable(AhbMstType())
    False

    But casting is allowed in all ways.

    >>> len(tuple(AhbSlvType().cast(AhbMstType())))
    14
    >>> len(tuple(AhbSlvType(proto=ahb5).cast(AhbMstType())))
    13
    >>> len(tuple(AhbSlvType(proto=ahb5).cast(AhbMstType(proto=ahb5))))
    14
    """

    title: str = "AHB Slave"
    comment: str = "AHB Slave"
    proto: AmbaProto = AMBA3

    def _build(self):
        # FWD
        self._add("hsel", AhbSelType())
        self._add("haddr", AhbAddrType())
        if self.proto.ausertype:
            self._add("hauser", self.proto.ausertype, title="AHB Address User Channel")
        self._add("hwrite", AhbWriteType())
        self._add("htrans", AhbTransType())
        self._add("hsize", AhbSizeType())
        self._add("hburst", AhbBurstType())
        self._add("hprot", AhbProtType())
        self._add("hwdata", AhbDataType())
        title: str = "AHB Transfer Done to Slave"
        self._add("hready", AhbReadyType(), title=title, comment=title)
        # BWD
        title: str = "AHB Transfer Done from Slave"
        self._add("hreadyout", AhbReadyType(), u.BWD, title=title, comment=title)
        self._add("hresp", AhbRespType(), u.BWD)
        self._add("hrdata", AhbDataType(), u.BWD)

    def cast(self, other):
        """
        How to cast an assign of type `self` from a value of type `other`.

        `self = cast(other)`
        """
        if isinstance(other, AhbSlvType) and self.proto != other.proto:
            # Drive a Slv with Slv signals
            yield "", ""
            yield "hsel", "hsel"
            yield "haddr", "haddr"
            # never use hauser
            yield "hwrite", "hwrite"
            yield "htrans", "htrans"
            yield "hsize", "hsize"
            yield "hburst", "hburst"
            yield "hprot", "hprot"
            yield "hwdata", "hwdata"
            yield "hready", "hready"
            # BWD
            yield "hreadyout", "hreadyout"
            yield "hresp", "hresp"
            yield "hrdata", "hrdata"
        elif isinstance(other, AhbMstType):
            # Drive a Slv with Mst signals
            yield "", ""
            yield "hsel", "ternary(htrans > '1b0', '1b1', '1b0')"
            yield "haddr", "haddr"
            if self.proto.ausertype == other.proto.ausertype:
                yield "hauser", "hauser"
            yield "hwrite", "hwrite"
            yield "htrans", "htrans"
            yield "hsize", "hsize"
            yield "hburst", "hburst"
            yield "hprot", "hprot"
            yield "hwdata", "hwdata"
            yield "hready", u.const("1'b1")
            # BWD
            yield "hreadyout", "hready"
            yield "hresp", "hresp"
            yield "hrdata", "hrdata"
        else:
            return None


class ApbSlvType(u.AStructType):
    """
    To APB Slave.

    Keyword Args:
        proto (Protocol): Protocol feature set selection.

    The default type:

    >>> for item in ApbSlvType().values(): item
    StructItem('paddr', ApbAddrType(32), doc=Doc(title='APB Bus Address', ...))
    StructItem('pwrite', ApbWriteType(), doc=Doc(title='APB Write Enable', ...))
    StructItem('pwdata', ApbDataType(32), doc=Doc(title='APB Data', ...))
    StructItem('penable', ApbEnaType(), doc=Doc(title='APB Transfer Enable', ...))
    StructItem('psel', ApbSelType(), doc=Doc(title='APB Slave Select', ...))
    StructItem('prdata', ApbDataType(32), orientation=BWD, doc=Doc(title='APB Data', ...))
    StructItem('pslverr', ApbRespType(), orientation=BWD, doc=Doc(title='APB Response Error', ...))
    StructItem('pready', ApbReadyType(), orientation=BWD, doc=Doc(title='APB Transfer Done', ...))

    With `pauser`:

    >>> class SecIdType(ASecIdType):
    ...     def _build(self):
    ...         self._add(0, "apps")
    ...         self._add(2, "comm")
    ...         self._add(5, "audio")
    >>> apb5 = AmbaProto("APB5", secidtype=SecIdType(default=2))

    >>> for item in ApbSlvType(proto=apb5).values(): item
    StructItem('paddr', ApbAddrType(32), doc=Doc(title='APB Bus Address', ...))
    StructItem('pauser', AuserType(4, default=2), doc=Doc(title='APB Address User Channel', ...))
    StructItem('pwrite', ApbWriteType(), doc=Doc(title='APB Write Enable', ...))
    StructItem('pwdata', ApbDataType(32), doc=Doc(title='APB Data', ...))
    StructItem('penable', ApbEnaType(), doc=Doc(title='APB Transfer Enable', ...))
    StructItem('psel', ApbSelType(), doc=Doc(title='APB Slave Select', ...))
    StructItem('prdata', ApbDataType(32), orientation=BWD, doc=Doc(title='APB Data', ...))
    StructItem('pslverr', ApbRespType(), orientation=BWD, doc=Doc(title='APB Response Error', ...))
    StructItem('pready', ApbReadyType(), orientation=BWD, doc=Doc(title='APB Transfer Done', ...))

    Both protocol versions are not connectable:

    >>> ApbSlvType().is_connectable(ApbSlvType(proto=apb5))
    False

    But casting is allowed:

    >>> for item in ApbSlvType().cast(ApbSlvType(proto=apb5)): item
    ('', '')
    ('paddr', 'paddr')
    ('pwrite', 'pwrite')
    ('pwdata', 'pwdata')
    ('penable', 'penable')
    ('psel', 'psel')
    ('prdata', 'prdata')
    ('pslverr', 'pslverr')
    ('pready', 'pready')
    """

    title: str = "APB Slave"
    comment: str = "APB Slave"
    proto: AmbaProto = AMBA3

    def _build(self):
        # FWD
        self._add("paddr", ApbAddrType())
        if self.proto.ausertype:
            self._add("pauser", self.proto.ausertype, title="APB Address User Channel")
        self._add("pwrite", ApbWriteType())
        self._add("pwdata", ApbDataType())
        self._add("penable", ApbEnaType())
        self._add("psel", ApbSelType())
        # BWD
        self._add("prdata", ApbDataType(), u.BWD)
        self._add("pslverr", ApbRespType(), u.BWD)
        self._add("pready", ApbReadyType(), u.BWD)

    def cast(self, other):
        """
        How to cast an assign of type `self` from a value of type `other`.

        `self = cast(other)`
        """
        if isinstance(other, ApbSlvType) and self.proto != other.proto:
            # Drive a Slv with Slv signals
            yield "", ""
            yield "paddr", "paddr"
            # never use pauser
            yield "pwrite", "pwrite"
            yield "pwdata", "pwdata"
            yield "penable", "penable"
            yield "psel", "psel"
            # BWD
            yield "prdata", "prdata"
            yield "pslverr", "pslverr"
            yield "pready", "pready"
        else:
            return None


class AhbSelType(u.BitType):
    """AHB Select."""

    title: str = "AHB Slave Select"
    comment: str = "AHB Slave Select"


class AhbAddrType(u.UintType):
    """
    Address.

    >>> AhbAddrType().width
    32
    >>> AhbAddrType(width=16).width
    16
    """

    title: str = "AHB Bus Address"
    comment: str = "AHB Bus Address"

    def __init__(self, width=32, **kwargs):
        super().__init__(width=width, **kwargs)


class AhbWordAddrType(u.UintType):
    """
    AHB Word Address.

    >>> AhbWordAddrType().width
    30
    """

    title: str = "AHB Word Address"
    comment: str = "AHB Word Address"

    def __init__(self, width=30, **kwargs):
        super().__init__(width=width, **kwargs)


class AhbHalfWordAddrType(u.UintType):
    """
    AHB Half Word Address.

    >>> AhbHalfWordAddrType().width
    31
    """

    title: str = "AHB Half Word Address"
    comment: str = "AHB Half Word Address"

    def __init__(self, width=31, **kwargs):
        super().__init__(width=width, **kwargs)


class AhbDataType(u.UintType):
    """
    AHB Data.

    >>> AhbDataType().width
    32
    >>> AhbDataType(width=64).width
    64
    """

    title: str = "AHB Data"
    comment: str = "AHB Data"

    def __init__(self, width=32, **kwargs):
        super().__init__(width=width, **kwargs)


class AhbTransType(u.AEnumType):
    """
    AHB Transfer Type.

    >>> for item in AhbTransType().values(): item
    EnumItem(0, 'idle', doc=Doc(title='No transfer'))
    EnumItem(1, 'busy', doc=Doc(title='Idle cycle within transfer'))
    EnumItem(2, 'nonseq', doc=Doc(title='Single transfer or first transfer of a burst'))
    EnumItem(3, 'seq', doc=Doc(title='Consecutive transfers of a burst'))
    """

    keytype: u.UintType = u.UintType(2)
    title: str = "AHB Transfer Type"
    comment: str = "AHB Transfer Type"

    def _build(self):
        self._add(0, "idle", "No transfer")
        self._add(1, "busy", "Idle cycle within transfer")
        self._add(2, "nonseq", "Single transfer or first transfer of a burst")
        self._add(3, "seq", "Consecutive transfers of a burst")


class AhbSizeType(u.AEnumType):
    """
    AHB Size Type.

    >>> for item in AhbSizeType().values(): item
    EnumItem(0, 'byte', doc=Doc(title='Byte', descr='8 bits'))
    EnumItem(1, 'halfword', doc=Doc(title='Halfword', descr='16 bits'))
    EnumItem(2, 'word', doc=Doc(title='Word', descr='32 bits'))
    EnumItem(3, 'doubleword', doc=Doc(title='Doubleword', descr='64 bits'))
    """

    keytype: u.UintType = u.UintType(3)
    title: str = "AHB Size"
    comment: str = "AHB Size"

    def _build(self):
        self._add(0, "byte", "Byte", descr="8 bits")
        self._add(1, "halfword", "Halfword", descr="16 bits")
        self._add(2, "word", "Word", descr="32 bits")
        self._add(3, "doubleword", "Doubleword", descr="64 bits")


class AhbBurstType(u.AEnumType):
    """
    AHB Burst Type.

    >>> for item in AhbBurstType().values(): item
    EnumItem(0, 'single', doc=Doc(title='Single transfer'))
    EnumItem(1, 'incr', doc=Doc(title='Incrementing burst of unspecified length'))
    EnumItem(2, 'wrap4', doc=Doc(title='4-beat wrapping burst'))
    EnumItem(3, 'incr4', doc=Doc(title='4-beat incrementing burst'))
    EnumItem(4, 'wrap8', doc=Doc(title='8-beat wrapping burst'))
    EnumItem(5, 'incr8', doc=Doc(title='8-beat incrementing burst'))
    EnumItem(6, 'wrap16', doc=Doc(title='16-beat wrapping burst'))
    EnumItem(7, 'incr16', doc=Doc(title='16-beat incrementing burst'))
    """

    keytype: u.UintType = u.UintType(3)
    title: str = "AHB Burst Type"
    comment: str = "AHB Burst Type"

    def _build(self):
        self._add(0, "single", "Single transfer")
        self._add(1, "incr", "Incrementing burst of unspecified length")
        self._add(2, "wrap4", "4-beat wrapping burst")
        self._add(3, "incr4", "4-beat incrementing burst")
        self._add(4, "wrap8", "8-beat wrapping burst")
        self._add(5, "incr8", "8-beat incrementing burst")
        self._add(6, "wrap16", "16-beat wrapping burst")
        self._add(7, "incr16", "16-beat incrementing burst")


class AhbProtType(u.UintType):
    """AHB Protection."""

    title: str = "AHB Transfer Protection"
    comment: str = "AHB Transfer Protection"

    def __init__(self, width=4, **kwargs):
        super().__init__(width=width, **kwargs)


class AhbWriteType(u.AEnumType):
    """
    AHB Write Type.

    >>> for item in AhbWriteType().values(): item
    EnumItem(0, 'read', doc=Doc(title='Read operation'))
    EnumItem(1, 'write', doc=Doc(title='Write operation'))
    """

    keytype: u.BitType = u.BitType()
    title: str = "AHB Write Enable"
    comment: str = "AHB Write Enable"

    def _build(self):
        self._add(0, "read", "Read operation")
        self._add(1, "write", "Write operation")


class AhbRespType(u.AEnumType):
    """
    AHB Response Type.

    >>> for item in AhbRespType().values(): item
    EnumItem(0, 'okay', doc=Doc(title='OK'))
    EnumItem(1, 'error', doc=Doc(title='Error'))
    """

    keytype: u.BitType = u.BitType()
    title: str = "AHB Response Error"
    comment: str = "AHB Response Error"

    def _build(self):
        self._add(0, "okay", "OK")
        self._add(1, "error", "Error")


class AhbReadyType(u.AEnumType):
    """
    AHB Ready Type.

    >>> for item in AhbReadyType().values(): item
    EnumItem(0, 'busy', doc=Doc(title='Ongoing'))
    EnumItem(1, 'done', doc=Doc(title='Done'))
    """

    keytype: u.BitType = u.BitType(default=1)
    title: str = "AHB Transfer Done"
    comment: str = "AHB Transfer Done"

    def _build(self):
        self._add(0, "busy", "Ongoing")
        self._add(1, "done", "Done")


class ApbSelType(u.BitType):
    """APB Select."""

    title: str = "APB Slave Select"
    comment: str = "APB Slave Select"


class ApbEnaType(u.EnaType):
    """APB Enable."""

    title: str = "APB Transfer Enable"
    comment: str = "APB Transfer Enable"


class ApbAddrType(u.UintType):
    """
    APB Address.

    >>> ApbAddrType().width
    32
    >>> ApbAddrType(width=16).width
    16
    """

    title: str = "APB Bus Address"
    comment: str = "APB Bus Address"

    def __init__(self, width=32, **kwargs):
        super().__init__(width=width, **kwargs)


class ApbDataType(u.UintType):
    """
    APB Data.

    >>> AhbDataType().width
    32
    >>> AhbDataType(width=64).width
    64
    """

    title: str = "APB Data"
    comment: str = "APB Data"

    def __init__(self, width=32, **kwargs):
        super().__init__(width=width, **kwargs)


class ApbWriteType(u.AEnumType):
    """
    AHB Write Type.

    >>> for item in ApbWriteType().values(): item
    EnumItem(0, 'read', doc=Doc(title='Read operation'))
    EnumItem(1, 'write', doc=Doc(title='Write operation'))
    """

    keytype: u.BitType = u.BitType()
    title: str = "APB Write Enable"
    comment: str = "APB Write Enable"

    def _build(self):
        self._add(0, "read", "Read operation")
        self._add(1, "write", "Write operation")


class ApbRespType(u.AEnumType):
    """
    APB Response Type.

    >>> for item in ApbRespType().values(): item
    EnumItem(0, 'okay', doc=Doc(title='OK'))
    EnumItem(1, 'error', doc=Doc(title='Error'))
    """

    keytype: u.BitType = u.BitType()
    title: str = "APB Response Error"
    comment: str = "APB Response Error"

    def _build(self):
        self._add(0, "okay", "OK")
        self._add(1, "error", "Error")


class ApbReadyType(u.AEnumType):
    """
    APB Ready Type.

    >>> for item in ApbReadyType().values(): item
    EnumItem(0, 'busy', doc=Doc(title='Ongoing'))
    EnumItem(1, 'done', doc=Doc(title='Done'))
    """

    keytype: u.BitType = u.BitType(default=1)
    title: str = "APB Transfer Done"
    comment: str = "APB Transfer Done"

    def _build(self):
        self._add(0, "busy", "Ongoing")
        self._add(1, "done", "Done")


class IdleType(u.AEnumType):
    """
    Bus Idle Type.

    for item in IdleType().values(): item
    EnumItem(0, 'busy', doc=Doc(title='Ongoing'))
    EnumItem(1, 'done', doc=Doc(title='Done'))
    """

    keytype: u.BitType = u.BitType(default=1)
    title: str = "Bus Idle"
    comment: str = "Bus Idle"

    def _build(self):
        self._add(0, "busy", "Busy", comment="Transfers Ongoing")
        self._add(1, "idle", "Idle")
