from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:NR:NEGativ:CURRent \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.aclr.nr.negativ.current.fetch() \n
		Return the ACLR for the first adjacent NR channel above (POSitiv) or below (NEGativ) the carrier frequency for NR
		standalone mode, for all measured list mode segments. The values described below are returned by FETCh commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:return: nr_negativ: float Comma-separated list of values, one per measured segment Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:NR:NEGativ:CURRent?', suppressed)
		return response

	# noinspection PyTypeChecker
	def calculate(self) -> List[enums.ResultStatus2]:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:NR:NEGativ:CURRent \n
		Snippet: value: List[enums.ResultStatus2] = driver.nrSubMeas.multiEval.listPy.aclr.nr.negativ.current.calculate() \n
		Return the ACLR for the first adjacent NR channel above (POSitiv) or below (NEGativ) the carrier frequency for NR
		standalone mode, for all measured list mode segments. The values described below are returned by FETCh commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:return: nr_negativ: float Comma-separated list of values, one per measured segment Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:NR:NEGativ:CURRent?', suppressed)
		return Conversions.str_to_list_enum(response, enums.ResultStatus2)
