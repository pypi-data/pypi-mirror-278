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
// Module:     ucdp_amba.ucdp_ahb_ml_example_ml
// Data Model: ucdp_amba.ucdp_ahb_ml.UcdpAhbMlMod
//
//
// Protocol: AmbaProto('')
//
//
//  Master > Slave    ram    periph    misc
// ----------------  -----  --------  ------
//       ext           X
//       dsp           X       X
//
//
// Size: 3.75 GB
//
// | Addrspace | Type  | Base       | Size             | Attributes |
// | --------- | ----  | ----       | ----             | ---------- |
// | ram       | Slave | 0xF0000000 | 16384x32 (64 KB) |            |
// | periph    | Slave | 0xF0010000 | 16384x32 (64 KB) |            |
// | misc      | Slave | 0xF0020000 | 8192x32 (32 KB)  |            |
//
//
// | Addrspace | Word | Field | Offset     | Access | Reset | Attributes |
// | --------- | ---- | ----- | ------     | ------ | ----- | ---------- |
// | ram       |      |       | 0xF0000000 |        |       |            |
// | periph    |      |       | 0xF0010000 |        |       |            |
// | misc      |      |       | 0xF0020000 |        |       |            |
//
// =============================================================================

`begin_keywords 1800-2009
`default_nettype none

module ucdp_ahb_ml_example_ml ( // ucdp_amba.ucdp_ahb_ml.UcdpAhbMlMod
  // main_i
  input  wire         main_clk_i,
  input  wire         main_rst_an_i,              // Async Reset (Low-Active)
  // ahb_mst_ext_i: AHB Input 'ext'
  input  wire  [1:0]  ahb_mst_ext_htrans_i,       // AHB Transfer Type
  input  wire  [31:0] ahb_mst_ext_haddr_i,        // AHB Bus Address
  input  wire         ahb_mst_ext_hwrite_i,       // AHB Write Enable
  input  wire  [2:0]  ahb_mst_ext_hsize_i,        // AHB Size
  input  wire  [2:0]  ahb_mst_ext_hburst_i,       // AHB Burst Type
  input  wire  [3:0]  ahb_mst_ext_hprot_i,        // AHB Transfer Protection
  input  wire  [31:0] ahb_mst_ext_hwdata_i,       // AHB Data
  output logic        ahb_mst_ext_hready_o,       // AHB Transfer Done
  output logic        ahb_mst_ext_hresp_o,        // AHB Response Error
  output logic [31:0] ahb_mst_ext_hrdata_o,       // AHB Data
  // ahb_mst_dsp_i: AHB Input 'dsp'
  input  wire  [1:0]  ahb_mst_dsp_htrans_i,       // AHB Transfer Type
  input  wire  [31:0] ahb_mst_dsp_haddr_i,        // AHB Bus Address
  input  wire         ahb_mst_dsp_hwrite_i,       // AHB Write Enable
  input  wire  [2:0]  ahb_mst_dsp_hsize_i,        // AHB Size
  input  wire  [2:0]  ahb_mst_dsp_hburst_i,       // AHB Burst Type
  input  wire  [3:0]  ahb_mst_dsp_hprot_i,        // AHB Transfer Protection
  input  wire  [31:0] ahb_mst_dsp_hwdata_i,       // AHB Data
  output logic        ahb_mst_dsp_hready_o,       // AHB Transfer Done
  output logic        ahb_mst_dsp_hresp_o,        // AHB Response Error
  output logic [31:0] ahb_mst_dsp_hrdata_o,       // AHB Data
  // ahb_slv_ram_o: AHB Output 'ram'
  output logic        ahb_slv_ram_hsel_o,         // AHB Slave Select
  output logic [31:0] ahb_slv_ram_haddr_o,        // AHB Bus Address
  output logic        ahb_slv_ram_hwrite_o,       // AHB Write Enable
  output logic [1:0]  ahb_slv_ram_htrans_o,       // AHB Transfer Type
  output logic [2:0]  ahb_slv_ram_hsize_o,        // AHB Size
  output logic [2:0]  ahb_slv_ram_hburst_o,       // AHB Burst Type
  output logic [3:0]  ahb_slv_ram_hprot_o,        // AHB Transfer Protection
  output logic [31:0] ahb_slv_ram_hwdata_o,       // AHB Data
  output logic        ahb_slv_ram_hready_o,       // AHB Transfer Done to Slave
  input  wire         ahb_slv_ram_hreadyout_i,    // AHB Transfer Done from Slave
  input  wire         ahb_slv_ram_hresp_i,        // AHB Response Error
  input  wire  [31:0] ahb_slv_ram_hrdata_i,       // AHB Data
  // ahb_slv_periph_o: AHB Output 'periph'
  output logic        ahb_slv_periph_hsel_o,      // AHB Slave Select
  output logic [31:0] ahb_slv_periph_haddr_o,     // AHB Bus Address
  output logic        ahb_slv_periph_hwrite_o,    // AHB Write Enable
  output logic [1:0]  ahb_slv_periph_htrans_o,    // AHB Transfer Type
  output logic [2:0]  ahb_slv_periph_hsize_o,     // AHB Size
  output logic [2:0]  ahb_slv_periph_hburst_o,    // AHB Burst Type
  output logic [3:0]  ahb_slv_periph_hprot_o,     // AHB Transfer Protection
  output logic [31:0] ahb_slv_periph_hwdata_o,    // AHB Data
  output logic        ahb_slv_periph_hready_o,    // AHB Transfer Done to Slave
  input  wire         ahb_slv_periph_hreadyout_i, // AHB Transfer Done from Slave
  input  wire         ahb_slv_periph_hresp_i,     // AHB Response Error
  input  wire  [31:0] ahb_slv_periph_hrdata_i,    // AHB Data
  // ahb_slv_misc_o: AHB Output 'misc'
  output logic        ahb_slv_misc_hsel_o,        // AHB Slave Select
  output logic [31:0] ahb_slv_misc_haddr_o,       // AHB Bus Address
  output logic        ahb_slv_misc_hwrite_o,      // AHB Write Enable
  output logic [1:0]  ahb_slv_misc_htrans_o,      // AHB Transfer Type
  output logic [2:0]  ahb_slv_misc_hsize_o,       // AHB Size
  output logic [2:0]  ahb_slv_misc_hburst_o,      // AHB Burst Type
  output logic [3:0]  ahb_slv_misc_hprot_o,       // AHB Transfer Protection
  output logic [31:0] ahb_slv_misc_hwdata_o,      // AHB Data
  output logic        ahb_slv_misc_hready_o,      // AHB Transfer Done to Slave
  input  wire         ahb_slv_misc_hreadyout_i,   // AHB Transfer Done from Slave
  input  wire         ahb_slv_misc_hresp_i,       // AHB Response Error
  input  wire  [31:0] ahb_slv_misc_hrdata_i       // AHB Data
);

// TODO

endmodule // ucdp_ahb_ml_example_ml

`default_nettype wire
`end_keywords
