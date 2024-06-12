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
// Module:     ucdp_amba.ucdp_ahb2apb_example_odd
// Data Model: ucdp_amba.ucdp_ahb2apb.UcdpAhb2apbMod
//
//
// Size: 36 KB
//
// | Addrspace | Type  | Base    | Size            | Attributes |
// | --------- | ----  | ----    | ----            | ---------- |
// | foo       | Slave | +0x0    | 1024x32 (4 KB)  | Sub        |
// | bar       | Slave | +0x1000 | 1024x32 (4 KB)  | Sub        |
// | baz       | Slave | +0x4000 | 3328x32 (13 KB) | Sub        |
// | bar       | Slave | +0x8000 | 1024x32 (4 KB)  | Sub        |
//
// =============================================================================

`begin_keywords 1800-2009
`default_nettype none

module ucdp_ahb2apb_example_odd ( // ucdp_amba.ucdp_ahb2apb.UcdpAhb2apbMod
  // main_i
  input  wire         main_clk_i,
  input  wire         main_rst_an_i,         // Async Reset (Low-Active)
  // ahb_slv_i: AHB Slave
  input  wire         ahb_slv_hsel_i,        // AHB Slave Select
  input  wire  [31:0] ahb_slv_haddr_i,       // AHB Bus Address
  input  wire         ahb_slv_hwrite_i,      // AHB Write Enable
  input  wire  [1:0]  ahb_slv_htrans_i,      // AHB Transfer Type
  input  wire  [2:0]  ahb_slv_hsize_i,       // AHB Size
  input  wire  [2:0]  ahb_slv_hburst_i,      // AHB Burst Type
  input  wire  [3:0]  ahb_slv_hprot_i,       // AHB Transfer Protection
  input  wire  [31:0] ahb_slv_hwdata_i,      // AHB Data
  input  wire         ahb_slv_hready_i,      // AHB Transfer Done to Slave
  output logic        ahb_slv_hreadyout_o,   // AHB Transfer Done from Slave
  output logic        ahb_slv_hresp_o,       // AHB Response Error
  output logic [31:0] ahb_slv_hrdata_o,      // AHB Data
  // apb_slv_foo_o: APB Slave 'foo'
  output logic [31:0] apb_slv_foo_paddr_o,   // APB Bus Address
  output logic        apb_slv_foo_pwrite_o,  // APB Write Enable
  output logic [31:0] apb_slv_foo_pwdata_o,  // APB Data
  output logic        apb_slv_foo_penable_o, // APB Transfer Enable
  output logic        apb_slv_foo_psel_o,    // APB Slave Select
  input  wire  [31:0] apb_slv_foo_prdata_i,  // APB Data
  input  wire         apb_slv_foo_pslverr_i, // APB Response Error
  input  wire         apb_slv_foo_pready_i,  // APB Transfer Done
  // apb_slv_bar_o: APB Slave 'bar'
  output logic [31:0] apb_slv_bar_paddr_o,   // APB Bus Address
  output logic        apb_slv_bar_pwrite_o,  // APB Write Enable
  output logic [31:0] apb_slv_bar_pwdata_o,  // APB Data
  output logic        apb_slv_bar_penable_o, // APB Transfer Enable
  output logic        apb_slv_bar_psel_o,    // APB Slave Select
  input  wire  [31:0] apb_slv_bar_prdata_i,  // APB Data
  input  wire         apb_slv_bar_pslverr_i, // APB Response Error
  input  wire         apb_slv_bar_pready_i,  // APB Transfer Done
  // apb_slv_baz_o: APB Slave 'baz'
  output logic [31:0] apb_slv_baz_paddr_o,   // APB Bus Address
  output logic        apb_slv_baz_pwrite_o,  // APB Write Enable
  output logic [31:0] apb_slv_baz_pwdata_o,  // APB Data
  output logic        apb_slv_baz_penable_o, // APB Transfer Enable
  output logic        apb_slv_baz_psel_o,    // APB Slave Select
  input  wire  [31:0] apb_slv_baz_prdata_i,  // APB Data
  input  wire         apb_slv_baz_pslverr_i, // APB Response Error
  input  wire         apb_slv_baz_pready_i   // APB Transfer Done
);

// TODO

endmodule // ucdp_ahb2apb_example_odd

`default_nettype wire
`end_keywords
