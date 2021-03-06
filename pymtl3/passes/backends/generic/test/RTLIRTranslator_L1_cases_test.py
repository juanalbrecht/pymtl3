#=========================================================================
# RTLIRTranslator_L1_cases_test.py
#=========================================================================
# Author : Peitian Pan
# Date   : May 23, 2019
"""Test the RTLIR translator."""

import pytest

from pymtl3.passes.rtlir.util.test_utility import expected_failure, get_parameter

from ..behavioral.test.BehavioralTranslatorL1_test import test_generic_behavioral_L1
from ..errors import RTLIRTranslationError
from ..structural.test.StructuralTranslatorL1_test import test_generic_structural_L1
from ..testcases import (
    CaseBitSelOverBitSelComp,
    CaseBitSelOverPartSelComp,
    CasePartSelOverBitSelComp,
    CasePartSelOverPartSelComp,
)
from .TestRTLIRTranslator import TestRTLIRTranslator


def run_test( case, m ):
  if not m._dsl.constructed:
    m.elaborate()
  tr = TestRTLIRTranslator(m)
  tr.translate( m )
  src = tr.hierarchy.src
  assert src == case.REF_SRC

@pytest.mark.parametrize(
  'case', get_parameter('case', test_generic_behavioral_L1) + \
          get_parameter('case', test_generic_structural_L1)
)
def test_generic_L1( case ):
  run_test( case, case.DUT() )

def test_bit_sel_over_bit_sel():
  with expected_failure( RTLIRTranslationError, "over bit/part selection" ):
    run_test( CaseBitSelOverBitSelComp, CaseBitSelOverBitSelComp.DUT() )

def test_bit_sel_over_part_sel():
  with expected_failure( RTLIRTranslationError, "over bit/part selection" ):
    run_test( CaseBitSelOverPartSelComp, CaseBitSelOverPartSelComp.DUT() )

def test_part_sel_over_bit_sel():
  with expected_failure( RTLIRTranslationError, "over bit/part selection" ):
    run_test( CasePartSelOverBitSelComp, CasePartSelOverBitSelComp.DUT() )

def test_part_sel_over_part_sel():
  with expected_failure( RTLIRTranslationError, "over bit/part selection" ):
    run_test( CasePartSelOverPartSelComp, CasePartSelOverPartSelComp.DUT() )
