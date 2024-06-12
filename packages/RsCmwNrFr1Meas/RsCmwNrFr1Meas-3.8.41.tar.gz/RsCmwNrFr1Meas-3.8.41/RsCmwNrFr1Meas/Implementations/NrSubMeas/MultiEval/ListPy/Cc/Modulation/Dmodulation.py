from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmodulationCls:
	"""Dmodulation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmodulation", core, parent)

	# noinspection PyTypeChecker
	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> List[enums.Modulation]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:MODulation:DMODulation \n
		Snippet: value: List[enums.Modulation] = driver.nrSubMeas.multiEval.listPy.cc.modulation.dmodulation.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return the detected modulation scheme for all measured list mode segments, for carrier <c>. The result is determined from
		the last measured slot of the statistical length of a segment. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: modulation: BPSK | BPWS | QPSK | Q16 | Q64 | Q256 Comma-separated list of values, one per measured segment BPSK, BPWS: Pi/2-BPSK, Pi/2-BPSK with shaping QPSK, Q16, Q64, Q256: QPSK, 16-QAM, 64-QAM, 256-QAM"""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:MODulation:DMODulation?', suppressed)
		return Conversions.str_to_list_enum(response, enums.Modulation)
