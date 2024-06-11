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
"""Test SvExprResolver."""

import ucdp as u
import ucdpsv as usv
from pytest import fixture


@fixture
def rslvr():
    """Default Resolver."""
    yield usv.SvExprResolver()


def test_basic(rslvr):
    """Basic Testing."""
    assert rslvr.namespace is None


def test_const(rslvr):
    """Constants."""
    resolve = rslvr.resolve
    assert resolve(u.ConstExpr(u.BitType())) == "1'b0"
    assert resolve(u.ConstExpr(u.BitType(default=1))) == "1'b1"
    assert resolve(u.ConstExpr(u.UintType(18, default=5))) == "18'h00005"
    assert resolve(u.ConstExpr(u.UintType(4, default=5))) == "4'h5"
    assert resolve(u.ConstExpr(u.SintType(18, default=5))) == "18'sh00005"
    assert resolve(u.ConstExpr(u.SintType(4, default=5))) == "4'sh5"


def test_get_ident_expr(rslvr):
    """get_ident_expr."""
    get_ident_expr = rslvr.get_ident_expr

    assert get_ident_expr(u.UintType(5), "ident", None) is None
    assert get_ident_expr(u.UintType(5, default=2), "ident", 0) == "5'h00"
    assert get_ident_expr(u.UintType(5, default=2), "ident", 1) == "5'h1F"
    assert get_ident_expr(u.SintType(5, default=-2), "ident", 0) == "5'sh00"
    assert get_ident_expr(u.SintType(5, default=-2), "ident", 1) == "5'sh0F"
    assert get_ident_expr(u.SintType(5, default=-2), "ident", "") == "ident"
    assert get_ident_expr(u.SintType(5, default=-2), "ident", "~") == "~ident"
