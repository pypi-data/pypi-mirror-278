##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2024, RISCY-Lib Contributors                             #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""Module to test the the ability of RTLPY to build a UVM_RAL from a MemoryMap definition
"""

import rtlpy.design as design
import rtlpy.uvm as uvm


def test_UVMReg():
  reg = design.Register("test_reg")
  ral_str = uvm.reg_to_ral(reg, 32)
  assert ral_str == """/** test_reg - UVM register model
 * Fields:
 */
class test_reg_reg extends uvm_reg;
  `uvm_object_utils(test_reg_reg)


  // CVR Field Vals Group
  covergroup cg_vals;
    option.per_instance = 1;

  endgroup

  // Create new register
  function new (string name = "test_reg_reg");
    super.new(name, 32, build_coverage(UVM_NO_COVERAGE));
    add_coverage(build_coverage(UVM_NO_COVERAGE));

    if (has_coverage(UVM_CVR_FIELD_VALS)) begin
      cg_vals = new();
      cg_vals.set_inst_name({get_full_name(), "_cg_vals"});
    end
  endfunction

  // Build all register field objects
  virtual function void build ();

    set_coverage(UVM_NO_COVERAGE);
  endfunction


  // The register sample function
  virtual function void sample_values();
    super.sample_values();

    if (has_coverage(UVM_CVR_FIELD_VALS))
      cg_vals.sample();
  endfunction
endclass"""


def test_TrafficLightFullRAL(traffic_light_full_def, traffic_light_ral):
  mem_map = design.AddressBlock.from_dict(traffic_light_full_def)

  ral_str = uvm.addrblock_to_ral(mem_map)

  assert ral_str == traffic_light_ral


def test_PagedBlockRAL(paged_block_ral):
  mem_map = design.PagedAddressBlock("test_paged_block", 32, 32)

  sblock1 = design.AddressBlock("subblock1", 32, 32)
  sblock1.add_register(design.Register("subblock1_reg1"))
  sblock1.add_register(design.Register("subblock1_reg2"))

  sblock2 = design.AddressBlock("subblock2", 32, 32)
  sblock2.add_register(design.Register("subblock2_reg1"))
  sblock2.add_register(design.Register("subblock2_reg2"))
  sblock2.dimension = 4

  mem_map.add_subblock(sblock1)
  mem_map.add_subblock(sblock2, 0x10)

  page_reg = design.Register("page_reg")
  page_reg.add_field(design.Field("page", 4, design.AccessType.READ_WRITE, 0))
  mem_map.page_reg = page_reg
  mem_map.page_reg_offset = 0x100

  assert paged_block_ral == uvm.addrblock_to_ral(mem_map)
