#=========================================================================
# SVTranslator_L1_cases_test.py
#=========================================================================
"""Test the SystemVerilog translator."""

import pytest

from pymtl3.passes.backends.utils.test_utility import check_eq
from pymtl3.passes.rtlir.utils.test_utility import get_parameter

from ..behavioral.test.SVBehavioralTranslatorL1_test import (
    test_sverilog_behavioral_L1 as behavioral,
)
from ..structural.test.SVStructuralTranslatorL1_test import (
    test_sverilog_structural_L1 as structural,
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
def test_sverilog_L1( case ):
  run_test( case, case.DUT() )
