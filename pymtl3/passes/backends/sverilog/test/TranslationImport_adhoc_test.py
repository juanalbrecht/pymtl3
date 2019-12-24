#=========================================================================
# TranslationImport_adhoc_test.py
#=========================================================================
# Author : Peitian Pan
# Date   : Jun 5, 2019
"""Test ad-hoc components with SystemVerilog translation and import."""

import pytest

from pymtl3.passes.rtlir.utils.test_utility import get_parameter
from pymtl3.stdlib.test import TestVectorSimulator

from .. import TranslationImportPass
from ..translation.behavioral.test.SVBehavioralTranslatorL1_test import (
    test_sverilog_behavioral_L1 as behavioral1,
)
from ..translation.behavioral.test.SVBehavioralTranslatorL2_test import (
    test_sverilog_behavioral_L2 as behavioral2,
)
from ..translation.behavioral.test.SVBehavioralTranslatorL3_test import (
    test_sverilog_behavioral_L3 as behavioral3,
)
from ..translation.behavioral.test.SVBehavioralTranslatorL4_test import (
    test_sverilog_behavioral_L4 as behavioral4,
)
from ..translation.behavioral.test.SVBehavioralTranslatorL5_test import (
    test_sverilog_behavioral_L5 as behavioral5,
)
from ..translation.structural.test.SVStructuralTranslatorL1_test import (
    test_sverilog_structural_L1 as structural1,
)
from ..translation.structural.test.SVStructuralTranslatorL2_test import (
    test_sverilog_structural_L2 as structural2,
)
from ..translation.structural.test.SVStructuralTranslatorL3_test import (
    test_sverilog_structural_L3 as structural3,
)
from ..translation.structural.test.SVStructuralTranslatorL4_test import (
    test_sverilog_structural_L4 as structural4,
)


def run_test( case ):
  try:
    _m = case.DUT()
    _m.elaborate()
    _m.sverilog_translate_import = True
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
  'case', get_parameter('case', behavioral1) + \
          get_parameter('case', behavioral2) + \
          get_parameter('case', behavioral3) + \
          get_parameter('case', behavioral4) + \
          get_parameter('case', behavioral5) + \
          get_parameter('case', structural1) + \
          get_parameter('case', structural2) + \
          get_parameter('case', structural3) + \
          get_parameter('case', structural4)
)
def test_sverilog_translation_import_adhoc( case ):
  run_test( case )
