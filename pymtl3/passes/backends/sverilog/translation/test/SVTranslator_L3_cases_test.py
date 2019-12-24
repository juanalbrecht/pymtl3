#=========================================================================
# SVTranslator_L3_cases_test.py
#=========================================================================
"""Test the SystemVerilog translator."""

import pytest

from pymtl3.passes.backends.utils.test_utility import check_eq
from pymtl3.passes.rtlir.utils.test_utility import get_parameter

from ..behavioral.test.SVBehavioralTranslatorL4_test import (
    test_sverilog_behavioral_L4 as behavioral,
)
from ..structural.test.SVStructuralTranslatorL3_test import (
    test_sverilog_structural_L3 as structural,
)
from ..SVTranslator import SVTranslator


def run_test( case, m ):
  m.elaborate()
  tr = SVTranslator( m )
  tr.translate( m )
  check_eq( tr.hierarchy.src, case.REF_SRC )

@pytest.mark.parametrize(
  'case', get_parameter('case', behavioral) + get_parameter('case', structural)
)
def test_sverilog_L3( case ):
  run_test( case, case.DUT() )
