// =============================================================================
//
// THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================
//
//  MIT License
//
//  Copyright (c) 2024 nbiotcloud
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.
//
// =============================================================================
//
// Module:     top.top_core
// Data Model: top.top.TopCoreMod
//
//
// =============================================================================


module top_core #( // top.top.TopCoreMod
  parameter integer       param_p = param_p,
  parameter integer       width_p = width_p,
  parameter signed  [7:0] other_p = 8'shFD
) (
  // main_i
  input  wire                main_clk_i,
  input  wire                main_rst_an_i,                    // Async Reset (Low-Active)
  input  wire  [param_p-1:0] p_i,
  output logic [param_p-1:0] p_o,
  input  wire  [width_p-1:0] data_i,
  output logic [width_p-1:0] data_o,
  input  wire  [2:0]         some_i,
  input  wire  [1:0]         bits_i,
  input  wire  [7:0]         array_i        [0:0+(param_p-1)],
  input  wire  [7:0]         array_open_i   [0:7],
  // intf_i: RX/TX
  output logic               intf_rx_o,
  input  wire                intf_tx_i
);


endmodule // top_core
