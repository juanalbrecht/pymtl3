#=========================================================================
# PyMTLBehavioralTranslatorL3.py
#=========================================================================
# Author : Peitian Pan
# Date   : Dec 23, 2019
"""Provide the level 3 PyMTL translator implementation."""

from pymtl3.passes.backends.generic.behavioral.BehavioralTranslatorL3 import (
    BehavioralTranslatorL3,
)
from pymtl3.passes.rtlir import RTLIRDataType as rdt
from pymtl3.passes.rtlir import RTLIRType as rt

from ...errors import PyMTLerilogTranslationError
from .PyMTLBehavioralTranslatorL2 import (
    BehavioralRTLIRToPyMTLVisitorL2,
    PyMTLBehavioralTranslatorL2,
)


class PyMTLBehavioralTranslatorL3(
    PyMTLBehavioralTranslatorL2, BehavioralTranslatorL3 ):

  def _get_rtlir2sv_visitor( s ):
    return BehavioralRTLIRToPyMTLVisitorL3

  def rtlir_tr_behavioral_freevar( s, id_, rtype, array_type, dtype, obj ):
    assert isinstance( rtype, rt.Const ), \
      f'{id_} freevar should be a constant!'
    if isinstance( rtype.get_dtype(), rdt.Struct ):
      return s.rtlir_tr_const_decl( f'__const__{id_}', rtype, array_type, dtype, obj )
    else:
      return super().rtlir_tr_behavioral_freevar(
          id_, rtype, array_type, dtype, obj )

#-------------------------------------------------------------------------
# BehavioralRTLIRToPyMTLVisitorL3
#-------------------------------------------------------------------------

class BehavioralRTLIRToPyMTLVisitorL3( BehavioralRTLIRToPyMTLVisitorL2 ):
  """Visitor that translates RTLIR to PyMTL for a single upblk."""

  #-----------------------------------------------------------------------
  # visit_StructInst
  #-----------------------------------------------------------------------

  def visit_StructInst( s, node ):
    values = list( map( s.visit, node.values ) )
    if len( values ) == 1:
      return values[0]
    else:
      cat_value = ", ".join( values )
      return f"{{ {cat_value} }}"

  #-----------------------------------------------------------------------
  # visit_Attribute
  #-----------------------------------------------------------------------

  def visit_Attribute( s, node ):
    """Return the PyMTL representation of an attribute.

    Add support for accessing struct attribute in L3.
    """
    if isinstance( node.value.Type, rt.Signal ):
      # if isinstance( node.value.Type, rt.Const ):
        # raise SVerilogTranslationError( s.blk, node,
          # "attribute ({}) of constant struct instance ({}) is not supported!". \
            # format( node.attr, node.value ))

      if isinstance( node.value.Type.get_dtype(), rdt.Struct ):
        value = s.visit( node.value )
        attr = node.attr
        s.check_res( node, attr )
        return f'{value}.{attr}'

    return super().visit_Attribute( node )
