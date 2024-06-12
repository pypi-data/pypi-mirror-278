from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DchTypeCls:
	"""DchType commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dchType", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> List[enums.ChannelTypeA]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:DCHType \n
		Snippet: value: List[enums.ChannelTypeA] = driver.nrSubMeas.multiEval.listPy.aclr.dchType.fetch() \n
		No command help available \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:return: channel_type: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:ACLR:DCHType?', suppressed)
		return Conversions.str_to_list_enum(response, enums.ChannelTypeA)
