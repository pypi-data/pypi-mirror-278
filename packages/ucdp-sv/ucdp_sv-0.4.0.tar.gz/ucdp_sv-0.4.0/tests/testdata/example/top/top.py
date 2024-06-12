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
"""UART Example."""

from typing import ClassVar

import ucdp as u
from fileliststandard import HdlFileList
from glbl.bus import BusType
from glbl.clk_gate import ClkGateMod


class IoType(u.AStructType):
    """IO."""

    title: str = "UART"
    comment: str = "RX/TX"

    def _build(self) -> None:
        self._add("rx", u.BitType(), u.BWD)
        self._add("tx", u.BitType(), u.FWD)


class TopMod(u.AMod):
    """Top Module."""

    filelists: ClassVar[u.ModFileLists] = (HdlFileList(gen="full"),)

    def _build(self) -> None:
        parser = self.parser

        param_p = self.add_param(u.IntegerType(default=10), "param_p")
        width_p = self.add_param(u.IntegerType(default=parser.log2(param_p + 1)), "width_p")
        default_p = self.add_param(u.UintType(param_p), "default_p")

        self.add_port(u.ClkRstAnType(), "main_i")
        self.add_port(IoType(), "intf_i", route="create(u_core/intf_i)")
        self.add_port(BusType(), "bus_i")

        self.add_port(u.UintType(param_p), "data_i")
        self.add_port(u.UintType(width_p), "cnt_o")

        self.add_const(u.UintType(param_p, default=default_p // 2), "const_c")

        clkgate = ClkGateMod(self, "u_clk_gate")
        clkgate.con("clk_i", "main_clk_i")
        clkgate.con("clk_o", "create(clk_s)")

        core = TopCoreMod(self, "u_core", paramdict={"width_p": width_p, "param_p": param_p})
        param_p = core.add_param(u.IntegerType(default=10), "param_p")
        width_p = core.add_param(u.IntegerType(default=8), "width_p")
        core.add_param(u.SintType(8, default=-3), "other_p")

        core.add_port(u.ClkRstAnType(), "main_i")
        core.add_port(u.UintType(param_p), "p_i")
        core.add_port(u.UintType(param_p), "p_o")
        core.add_port(u.UintType(width_p), "data_i")
        core.add_port(u.UintType(width_p), "data_o")
        core.add_port(u.UintType(3), "some_i")
        core.add_port(u.UintType(2), "bits_i")

        core.add_port(u.ArrayType(u.UintType(8), param_p), "array_i")
        core.add_port(u.ArrayType(u.UintType(8), 8), "array_open_i")
        core.con("array_i", "create(array_s)")

        core.con("main_clk_i", "clk_s")
        core.con("main_rst_an_i", "main_rst_an_i")

        core.con("some_i", "3h4")
        core.con("bits_i", "data_i[3:2]")


class TopCoreMod(u.ACoreMod):
    """Core Module."""

    filelists: ClassVar[u.ModFileLists] = (HdlFileList(gen="full"),)
