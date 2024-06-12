from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .........Internal.Types import DataType
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default, maximum=repcap.Maximum.Default) -> List[int]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:ESFLatness:SCINdex:MAXimum<nr>:CURRent \n
		Snippet: value: List[int] = driver.nrSubMeas.multiEval.listPy.cc.esFlatness.scIndex.maximum.current.fetch(carrierComponent = repcap.CarrierComponent.Default, maximum = repcap.Maximum.Default) \n
		Return subcarrier indices of the equalizer spectrum flatness measurement for all measured list mode segments, for carrier
		<c>. At these SC indices, the current MINimum or MAXimum power of the equalizer coefficients has been detected within the
		selected range. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param maximum: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Maximum')
			:return: maximum: No help available"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		maximum_cmd_val = self._cmd_group.get_repcap_cmd_value(maximum, repcap.Maximum)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_int_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:ESFLatness:SCINdex:MAXimum{maximum_cmd_val}:CURRent?', suppressed)
		return response
