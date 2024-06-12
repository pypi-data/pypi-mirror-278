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
// Module:     top.top
// Data Model: top.top.TopMod
//
// =============================================================================

`begin_keywords 1800-2009
`default_nettype none

module top #( // top.top.TopMod
  parameter integer               param_p   = 10,
  parameter integer               width_p   = $clog2(param_p + 1),
  parameter         [param_p-1:0] default_p = {param_p {1'b0}}
) (
  // main_i
  input  wire                main_clk_i,
  input  wire                main_rst_an_i, // Async Reset (Low-Active)
  // intf_i: RX/TX
  output logic               intf_rx_o,
  input  wire                intf_tx_i,
  // bus_i
  input  wire  [1:0]         bus_trans_i,
  input  wire  [31:0]        bus_addr_i,
  input  wire                bus_write_i,
  input  wire  [31:0]        bus_wdata_i,
  output logic               bus_ready_o,
  output logic               bus_resp_o,
  output logic [31:0]        bus_rdata_o,
  input  wire  [param_p-1:0] data_i,
  output logic [width_p-1:0] cnt_o
);



  // ------------------------------------------------------
  //  Local Parameter
  // ------------------------------------------------------
  localparam [param_p-1:0] const_c = default_p / param_p'd2;


  // ------------------------------------------------------
  //  Signals
  // ------------------------------------------------------
  logic       clk_s;
  logic [7:0] array_s [0:0+(param_p-1)];


  // ------------------------------------------------------
  //  glbl.clk_gate: u_clk_gate
  // ------------------------------------------------------
  clk_gate u_clk_gate (
    .clk_i(main_clk_i),
    .clk_o(clk_s     ),
    .ena_i(1'b0      )  // TODO
  );


  // ------------------------------------------------------
  //  top.top_core: u_core
  // ------------------------------------------------------
  top_core #(
    .param_p(10            ),
    .width_p($clog2(10 + 1))
  ) u_core (
    // main_i
    .main_clk_i   (clk_s        ),
    .main_rst_an_i(main_rst_an_i), // Async Reset (Low-Active)
    .p_i          ({10 {1'b0}}  ), // TODO
    .p_o          (             ), // TODO
    .data_i       ({8 {1'b0}}   ), // TODO
    .data_o       (             ), // TODO
    .some_i       (3'h4         ),
    .bits_i       (data_i[3:2]  ),
    .array_i      (array_s      ),
    .array_open_i ('{8{8'h00}}  ), // TODO
    // intf_i: RX/TX
    .intf_rx_o    (intf_rx_o    ),
    .intf_tx_i    (intf_tx_i    )
  );

endmodule // top

`default_nettype wire
`end_keywords
