from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SlotsCls:
	"""Slots commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("slots", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation:TRACe:PMONitor:SLOTs \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.trace.pmonitor.slots.read() \n
		Returns the power monitor results as power vs slot values (as in the result diagram) . The number of subframes per trace
		is configurable, see method RsCmwNrFr1Meas.Configure.NrSubMeas.MultiEval.nsubFrames. The number of slots per subframe
		depends on the SCS. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:return: power: float Comma-separated list of power values, one value per slot Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:NRSub:MEASurement<Instance>:MEValuation:TRACe:PMONitor:SLOTs?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:PMONitor:SLOTs \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.trace.pmonitor.slots.fetch() \n
		Returns the power monitor results as power vs slot values (as in the result diagram) . The number of subframes per trace
		is configurable, see method RsCmwNrFr1Meas.Configure.NrSubMeas.MultiEval.nsubFrames. The number of slots per subframe
		depends on the SCS. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:return: power: float Comma-separated list of power values, one value per slot Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:PMONitor:SLOTs?', suppressed)
		return response
