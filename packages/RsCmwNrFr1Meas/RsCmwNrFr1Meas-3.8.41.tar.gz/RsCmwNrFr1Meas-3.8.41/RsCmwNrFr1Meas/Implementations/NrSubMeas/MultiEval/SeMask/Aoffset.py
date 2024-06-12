from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AoffsetCls:
	"""Aoffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("aoffset", core, parent)

	def fetch(self) -> List[int]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:SEMask:AOFFset \n
		Snippet: value: List[int] = driver.nrSubMeas.multiEval.seMask.aoffset.fetch() \n
		No command help available \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:return: offset: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_int_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:SEMask:AOFFset?', suppressed)
		return response
