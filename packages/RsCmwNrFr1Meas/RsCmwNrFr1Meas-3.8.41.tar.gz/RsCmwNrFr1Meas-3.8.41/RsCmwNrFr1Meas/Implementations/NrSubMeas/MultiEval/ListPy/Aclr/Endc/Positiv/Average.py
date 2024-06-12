from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AverageCls:
	"""Average commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:ENDC:POSitiv:AVERage \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.aclr.endc.positiv.average.fetch() \n
		Return the ACLR for the adjacent channel above (POSitiv) or below (NEGativ) the carrier frequency for EN-DC mode, for all
		measured list mode segments. The values described below are returned by FETCh commands. CALCulate commands return limit
		check results instead, one value for each result listed below. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:return: nr_positiv: float Comma-separated list of values, one per measured segment Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:ENDC:POSitiv:AVERage?', suppressed)
		return response

	# noinspection PyTypeChecker
	def calculate(self) -> List[enums.ResultStatus2]:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:ENDC:POSitiv:AVERage \n
		Snippet: value: List[enums.ResultStatus2] = driver.nrSubMeas.multiEval.listPy.aclr.endc.positiv.average.calculate() \n
		Return the ACLR for the adjacent channel above (POSitiv) or below (NEGativ) the carrier frequency for EN-DC mode, for all
		measured list mode segments. The values described below are returned by FETCh commands. CALCulate commands return limit
		check results instead, one value for each result listed below. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:return: nr_positiv: float Comma-separated list of values, one per measured segment Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:ENDC:POSitiv:AVERage?', suppressed)
		return Conversions.str_to_list_enum(response, enums.ResultStatus2)
