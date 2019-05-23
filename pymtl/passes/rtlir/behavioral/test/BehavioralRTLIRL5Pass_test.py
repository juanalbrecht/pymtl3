#=========================================================================
# BehavioralRTLIRL5Pass_test.py
#=========================================================================
# Author : Peitian Pan
# Date   : Feb 2, 2019
"""Test the level 5 behavioral RTLIR passes.

The L5 generation, L5 type check, and visualization passes are invoked. The
generation pass results are verified against a reference AST.
"""

from __future__ import absolute_import, division, print_function

import pytest

from pymtl import *
from pymtl.passes.rtlir.behavioral import BehavioralRTLIRVisualizationPass
from pymtl.passes.rtlir.behavioral.BehavioralRTLIR import *
from pymtl.passes.rtlir.behavioral.BehavioralRTLIRGenL5Pass import (
    BehavioralRTLIRGenL5Pass,
)
from pymtl.passes.rtlir.behavioral.BehavioralRTLIRTypeCheckL5Pass import (
    BehavioralRTLIRTypeCheckL5Pass,
)
from pymtl.passes.rtlir.errors import PyMTLSyntaxError, PyMTLTypeError
from pymtl.passes.rtlir.test_utility import do_test, expected_failure


def local_do_test( m ):
  """Check if generated behavioral RTLIR is the same as reference."""
  m.elaborate()
  m.apply( BehavioralRTLIRGenL5Pass() )
  m.apply( BehavioralRTLIRTypeCheckL5Pass() )
  m.apply( BehavioralRTLIRVisualizationPass() )

  try:
    ref = m._rtlir_test_ref
    for blk in m.get_update_blocks():
      upblk = m._pass_behavioral_rtlir_gen.rtlir_upblks[ blk ]
      assert upblk == ref[ blk.__name__ ]
  except AttributeError:
    pass

#-------------------------------------------------------------------------
# Correct test cases
#-------------------------------------------------------------------------

def test_L5_component_attr( do_test ):
  class B( Component ):
    def construct( s ):
      s.out = OutPort( Bits32 )
  class A( Component ):
    def construct( s ):
      s.comp = B()
      s.out = OutPort( Bits32 )
      @s.update
      def upblk():
        s.out = s.comp.out
  a = A()
  a._rtlir_test_ref = { 'upblk' : CombUpblk( 'upblk', [ Assign(
      Attribute( Base( a ), 'out' ), Attribute(
        Attribute( Base( a ), 'comp' ), 'out' ) ) ] ) }
  do_test( a )

def test_L5_component_array_index( do_test ):
  class B( Component ):
    def construct( s ):
      s.out = OutPort( Bits32 )
  class A( Component ):
    def construct( s ):
      s.comp = [ B() for _ in xrange(4) ]
      s.out = OutPort( Bits32 )
      @s.update
      def upblk():
        s.out = s.comp[2].out
  a = A()
  a._rtlir_test_ref = { 'upblk' : CombUpblk( 'upblk', [ Assign(
      Attribute( Base( a ), 'out' ), Attribute( Index(
        Attribute( Base( a ), 'comp' ), Number(2) ), 'out' ) ) ] ) }
  do_test( a )

#-------------------------------------------------------------------------
# PyMTL type errors
#-------------------------------------------------------------------------

@pytest.mark.xfail( reason = "PyMTL DSL intercepted this error" )
def test_L5_component_no_field( do_test ):
  class B( Component ):
    def construct( s ):
      s.out = OutPort( Bits32 )
  class A( Component ):
    def construct( s ):
      s.comp = B()
      s.out = OutPort( Bits32 )
      @s.update
      def upblk():
        s.out = s.comp.bar
  with expected_failure( PyMTLTypeError, "comp does not have field bar" ):
    do_test( A() )

def test_L5_component_not_port( do_test ):
  class C( Component ):
    def construct( s ):
      s.c_out = OutPort( Bits32 )
  class B( Component ):
    def construct( s ):
      s.comp = C()
      s.b_out = OutPort( Bits32 )
  class A( Component ):
    def construct( s ):
      s.comp = B()
      s.a_out = OutPort( Bits32 )
      @s.update
      def upblk():
        s.a_out = s.comp.comp.c_out
  with expected_failure( PyMTLTypeError, "comp is not a port of subcomponent B" ):
    do_test( A() )