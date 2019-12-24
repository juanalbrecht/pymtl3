#=========================================================================
# PyMTLTranslator.py
#=========================================================================
# Author : Peitian Pan
# Date   : Dec 23, 2019
"""Provide PyMTL translator."""

from pymtl3.passes.backends.generic import RTLIRTranslator
from pymtl3.passes.backends.pymtl.utils.utility import pymtl_reserved

from .behavioral import PyMTLBehavioralTranslator
from .structural import PyMTLStructuralTranslator


class PyMTLTranslator(
    RTLIRTranslator, PyMTLStructuralTranslator, PyMTLBehavioralTranslator
  ):

  def get_pretty( s, namespace, attr, newline=True ):
    ret = getattr(namespace, attr, "")
    if newline and (ret and ret[-1] != '\n'):
      ret += "\n"
    return ret

  def is_pymtl_reserved( s, name ):
    return name in pymtl_reserved

  def set_header( s ):
    s.header = \
"""\
//-------------------------------------------------------------------------
// {name}.sv
//-------------------------------------------------------------------------
// This file is generated by PyMTL3 PyMTL translation pass.

"""

  def rtlir_tr_src_layout( s, hierarchy ):
    s.set_header()
    name = s._top_module_full_name
    ret = s.header.format( **locals() )

    # Add struct definitions
    for struct_dtype, tplt in hierarchy.decl_type_struct:
      template = \
"""\
// PyMTL BitStruct {dtype_name} Definition
// At {file_info}
{struct_def}\
"""
      dtype_name = struct_dtype.get_name()
      file_info = struct_dtype.get_file_info()
      struct_def = tplt['def'] + '\n'
      ret += template.format( **locals() )

    # Add component sources
    ret += hierarchy.component_src
    return ret

  def rtlir_tr_components( s, components ):
    return "\n\n".join( components )

  def rtlir_tr_component( s, behavioral, structural ):

    template =\
"""\
// PyMTL Component {component_name} Definition
// {optional_full_name}At {file_info}
module {module_name}
(
{ports});
{body}
endmodule
"""
    component_name = structural.component_name
    file_info = structural.component_file_info
    ports_template = "{port_decls}{ifc_decls}"
    full_name = structural.component_full_name
    module_name = structural.component_unique_name

    if full_name != module_name:
      optional_full_name = f"Full name: {full_name}\n// "
    else:
      optional_full_name = ""

    port_decls = s.get_pretty(structural, 'decl_ports', False)
    ifc_decls = s.get_pretty(structural, 'decl_ifcs', False)
    if port_decls or ifc_decls:
      if port_decls and ifc_decls:
        port_decls += ',\n'
      ifc_decls += '\n'
    ports = ports_template.format(**locals())

    const_decls = s.get_pretty(structural, "decl_consts")
    fvar_decls = s.get_pretty(behavioral, "decl_freevars")
    wire_decls = s.get_pretty(structural, "decl_wires")
    tmpvar_decls = s.get_pretty(behavioral, "decl_tmpvars")
    subcomp_decls = s.get_pretty(structural, "decl_subcomps")
    upblk_decls = s.get_pretty(behavioral, "upblk_decls")
    body = const_decls + fvar_decls + wire_decls + subcomp_decls \
         + tmpvar_decls + upblk_decls
    connections = s.get_pretty(structural, "connections")
    if (body and connections) or (not body and connections):
      connections = '\n' + connections
    body += connections

    s._top_module_name = structural.component_name
    s._top_module_full_name = module_name
    return template.format( **locals() )
