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
// Module:     ucdp_amba.ucdp_ahb2apb_example_ahb2apb_amba5_errirqfalse
// Data Model: ucdp_amba.ucdp_ahb2apb.UcdpAhb2apbMod
//
//
//
// Size: 12 KB
//
// | Namespace | Type  | Base    | Size           | Attributes |
// | --------- | ----  | ----    | ----           | ---------- |
// | default   | Slave | +0x0    | 1024x32 (4 KB) | Sub        |
// | slv3      | Slave | +0x1000 | 1024x32 (4 KB) | Sub        |
// | slv5      | Slave | +0x2000 | 1024x32 (4 KB) | Sub        |//
// =============================================================================


module ucdp_ahb2apb_example_ahb2apb_amba5_errirqfalse ( // ucdp_amba.ucdp_ahb2apb.UcdpAhb2apbMod
  // main_i
  input  wire         main_clk_i,
  input  wire         main_rst_an_i,             // Async Reset (Low-Active)
  // ahb_slv_i: AHB Slave
  input  wire         ahb_slv_hsel_i,            // AHB Slave Select
  input  wire  [31:0] ahb_slv_haddr_i,           // AHB Bus Address
  input  wire  [3:0]  ahb_slv_hauser_i,          // Address User Channel
  input  wire         ahb_slv_hwrite_i,          // AHB Write Enable
  input  wire  [1:0]  ahb_slv_htrans_i,          // AHB Transfer Type
  input  wire  [2:0]  ahb_slv_hsize_i,           // AHB Size
  input  wire  [2:0]  ahb_slv_hburst_i,          // AHB Burst Type
  input  wire  [3:0]  ahb_slv_hprot_i,           // AHB Transfer Protection
  input  wire  [31:0] ahb_slv_hwdata_i,          // AHB Data
  input  wire         ahb_slv_hready_i,          // AHB Transfer Done to Slave
  output logic        ahb_slv_hreadyout_o,       // AHB Transfer Done from Slave
  output logic        ahb_slv_hresp_o,           // AHB Response Error
  output logic [31:0] ahb_slv_hrdata_o,          // AHB Data
  // apb_slv_default_o: APB Slave 'default'
  output logic [31:0] apb_slv_default_paddr_o,   // APB Bus Address
  output logic [3:0]  apb_slv_default_pauser_o,  // Address User Channel
  output logic        apb_slv_default_pwrite_o,  // APB Write Enable
  output logic [31:0] apb_slv_default_pwdata_o,  // APB Data
  output logic        apb_slv_default_penable_o, // APB Transfer Enable
  output logic        apb_slv_default_psel_o,    // APB Slave Select
  input  wire  [31:0] apb_slv_default_prdata_i,  // APB Data
  input  wire         apb_slv_default_pslverr_i, // APB Response Error
  input  wire         apb_slv_default_pready_i,  // APB Transfer Done
  // apb_slv_slv3_o: APB Slave 'slv3'
  output logic [31:0] apb_slv_slv3_paddr_o,      // APB Bus Address
  output logic        apb_slv_slv3_pwrite_o,     // APB Write Enable
  output logic [31:0] apb_slv_slv3_pwdata_o,     // APB Data
  output logic        apb_slv_slv3_penable_o,    // APB Transfer Enable
  output logic        apb_slv_slv3_psel_o,       // APB Slave Select
  input  wire  [31:0] apb_slv_slv3_prdata_i,     // APB Data
  input  wire         apb_slv_slv3_pslverr_i,    // APB Response Error
  input  wire         apb_slv_slv3_pready_i,     // APB Transfer Done
  // apb_slv_slv5_o: APB Slave 'slv5'
  output logic [31:0] apb_slv_slv5_paddr_o,      // APB Bus Address
  output logic [3:0]  apb_slv_slv5_pauser_o,     // Address User Channel
  output logic        apb_slv_slv5_pwrite_o,     // APB Write Enable
  output logic [31:0] apb_slv_slv5_pwdata_o,     // APB Data
  output logic        apb_slv_slv5_penable_o,    // APB Transfer Enable
  output logic        apb_slv_slv5_psel_o,       // APB Slave Select
  input  wire  [31:0] apb_slv_slv5_prdata_i,     // APB Data
  input  wire         apb_slv_slv5_pslverr_i,    // APB Response Error
  input  wire         apb_slv_slv5_pready_i      // APB Transfer Done
);

// TODO

endmodule // ucdp_ahb2apb_example_ahb2apb_amba5_errirqfalse
