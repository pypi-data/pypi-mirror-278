from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StartCls:
	"""Start commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("start", core, parent)

	def fetch(self, sEGMent=repcap.SEGMent.Default) -> int:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>:PMONitor:ARRay:STARt \n
		Snippet: value: int = driver.nrSubMeas.multiEval.listPy.segment.pmonitor.array.start.fetch(sEGMent = repcap.SEGMent.Default) \n
		Returns the offset of the first power monitor vs subframe result for segment <no> within a result list for all measured
		segments. Such a result list is, for example, returned by the command method RsCmwNrFr1Meas.NrSubMeas.MultiEval.ListPy.
		Pmonitor.Rms.fetch. A returned <Start> value n indicates that the result for the first subframe of the segment is the
		(n+1) th result in the power result list over all segments. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: start: decimal Offset of the first power monitor vs subframe result."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:PMONitor:ARRay:STARt?', suppressed)
		return Conversions.str_to_int(response)
