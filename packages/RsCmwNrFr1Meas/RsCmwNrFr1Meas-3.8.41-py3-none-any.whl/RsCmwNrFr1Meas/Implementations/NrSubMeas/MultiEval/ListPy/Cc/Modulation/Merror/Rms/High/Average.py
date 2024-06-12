from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ..........Internal.Types import DataType
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AverageCls:
	"""Average commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:MODulation:MERRor:RMS:HIGH:AVERage \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.listPy.cc.modulation.merror.rms.high.average.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return magnitude error RMS values for low and high EVM window position, for all measured list mode segments, for carrier
		<c>. The values described below are returned by FETCh commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: mag_error_rms_high: float Comma-separated list of values, one per measured segment Unit: %"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:MODulation:MERRor:RMS:HIGH:AVERage?', suppressed)
		return response

	def calculate(self, carrierComponent=repcap.CarrierComponent.Default) -> List[float or bool]:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:MODulation:MERRor:RMS:HIGH:AVERage \n
		Snippet: value: List[float or bool] = driver.nrSubMeas.multiEval.listPy.cc.modulation.merror.rms.high.average.calculate(carrierComponent = repcap.CarrierComponent.Default) \n
		Return magnitude error RMS values for low and high EVM window position, for all measured list mode segments, for carrier
		<c>. The values described below are returned by FETCh commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: mag_error_rms_high: (float or boolean items) float Comma-separated list of values, one per measured segment Unit: %"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:MODulation:MERRor:RMS:HIGH:AVERage?', suppressed)
		return Conversions.str_to_float_or_bool_list(response)
