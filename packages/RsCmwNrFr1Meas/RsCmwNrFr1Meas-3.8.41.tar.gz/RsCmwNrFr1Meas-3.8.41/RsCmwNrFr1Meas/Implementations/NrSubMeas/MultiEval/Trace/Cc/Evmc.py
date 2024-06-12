from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EvmcCls:
	"""Evmc commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("evmc", core, parent)

	def read(self, carrierComponent=repcap.CarrierComponent.Default) -> List[float]:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation:TRACe[:CC<no>]:EVMC \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.trace.cc.evmc.read(carrierComponent = repcap.CarrierComponent.Default) \n
		Returns the values of the EVM vs subcarrier trace for carrier <no>. See also 'View EVM vs Subcarrier'. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: ratio: float Comma-separated list of EVM values, one value per subcarrier For not allocated subcarriers, NCAP is returned. Unit: %"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:NRSub:MEASurement<Instance>:MEValuation:TRACe:CC{carrierComponent_cmd_val}:EVMC?', suppressed)
		return response

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe[:CC<no>]:EVMC \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.trace.cc.evmc.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Returns the values of the EVM vs subcarrier trace for carrier <no>. See also 'View EVM vs Subcarrier'. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: ratio: float Comma-separated list of EVM values, one value per subcarrier For not allocated subcarriers, NCAP is returned. Unit: %"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:CC{carrierComponent_cmd_val}:EVMC?', suppressed)
		return response
