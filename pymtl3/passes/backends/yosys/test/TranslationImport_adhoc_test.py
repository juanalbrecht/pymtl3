#=========================================================================
# TranslationImport_adhoc_test.py
#=========================================================================
# Author : Peitian Pan
# Date   : Jun 15, 2019
"""Test ad-hoc components with yosys-SystemVerilog translation and import."""

import pytest

from pymtl3.passes.rtlir.utils.test_utility import get_parameter
from pymtl3.stdlib.test import TestVectorSimulator

from ..translation.behavioral.test.YosysBehavioralTranslatorL1_test import (
    test_yosys_behavioral_L1 as behavioral1,
)
from ..translation.behavioral.test.YosysBehavioralTranslatorL2_test import (
    test_yosys_behavioral_L2 as behavioral2,
)
from ..translation.behavioral.test.YosysBehavioralTranslatorL3_test import (
    test_yosys_behavioral_L3 as behavioral3,
)
from ..translation.behavioral.test.YosysBehavioralTranslatorL4_test import (
    test_yosys_behavioral_L4 as behavioral4,
)
from ..translation.behavioral.test.YosysBehavioralTranslatorL5_test import (
    test_yosys_behavioral_L5 as behavioral5,
)
from ..translation.structural.test.YosysStructuralTranslatorL1_test import (
    test_yosys_structural_L1 as structural1,
)
from ..translation.structural.test.YosysStructuralTranslatorL2_test import (
    test_yosys_structural_L2 as structural2,
)
from ..translation.structural.test.YosysStructuralTranslatorL3_test import (
    test_yosys_structural_L3 as structural3,
)
from ..translation.structural.test.YosysStructuralTranslatorL4_test import (
    test_yosys_structural_L4 as structural4,
)
from ..TranslationImportPass import TranslationImportPass

XFAILED_TESTS = [
    # incoherent translation result of Yosys backend
    # the translated design is correct after minor transformation
    # in logic synthesis, but verilator simulation is incorrect
    'CaseConnectLiteralStructComp',
]

def run_test( case ):
  try:
    _m = case.DUT()
    _m.elaborate()
    _m.yosys_translate_import = True
    m = TranslationImportPass()( _m )
    sim = TestVectorSimulator( m, case.TEST_VECTOR, case.TV_IN, case.TV_OUT )
    sim.run_test()
  finally:
    try:
      m.finalize()
    except UnboundLocalError:
      # This test fails due to translation errors
      pass

@pytest.mark.parametrize(
  'case', list(filter(lambda x: x.__name__ not in XFAILED_TESTS,
          get_parameter('case', behavioral1) + \
          get_parameter('case', behavioral2) + \
          get_parameter('case', behavioral3) + \
          get_parameter('case', behavioral4) + \
          get_parameter('case', behavioral5) + \
          get_parameter('case', structural1) + \
          get_parameter('case', structural2) + \
          get_parameter('case', structural3) + \
          get_parameter('case', structural4) ) )
)
def test_yosys_translation_import_adhoc( case ):
  run_test( case )
