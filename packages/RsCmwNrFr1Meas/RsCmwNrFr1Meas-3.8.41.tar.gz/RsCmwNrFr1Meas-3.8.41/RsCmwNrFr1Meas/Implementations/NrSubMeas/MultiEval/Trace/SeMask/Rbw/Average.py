from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AverageCls:
	"""Average commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	def read(self, rbw=repcap.Rbw.Default) -> List[float]:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW<kHz>:AVERage \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.trace.seMask.rbw.average.read(rbw = repcap.Rbw.Default) \n
		Returns the values of the spectrum emission traces. Separate traces are available for the individual resolution
		bandwidths (<kHz>) . The results of the current, average and maximum traces can be retrieved. See also 'View Spectrum
		Emission Mask'. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:param rbw: optional repeated capability selector. Default value: Bw1 (settable in the interface 'Rbw')
			:return: power: float Comma-separated list of power results The value in the middle of the result array corresponds to the center frequency. The test point separation between two results depends on the resolution bandwidth, see table below. If there is no result for a frequency because no limit is defined, INV is returned. Unit: dBm"""
		rbw_cmd_val = self._cmd_group.get_repcap_cmd_value(rbw, repcap.Rbw)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:NRSub:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW{rbw_cmd_val}:AVERage?', suppressed)
		return response

	def fetch(self, rbw=repcap.Rbw.Default) -> List[float]:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW<kHz>:AVERage \n
		Snippet: value: List[float] = driver.nrSubMeas.multiEval.trace.seMask.rbw.average.fetch(rbw = repcap.Rbw.Default) \n
		Returns the values of the spectrum emission traces. Separate traces are available for the individual resolution
		bandwidths (<kHz>) . The results of the current, average and maximum traces can be retrieved. See also 'View Spectrum
		Emission Mask'. \n
		Use RsCmwNrFr1Meas.reliability.last_value to read the updated reliability indicator. \n
			:param rbw: optional repeated capability selector. Default value: Bw1 (settable in the interface 'Rbw')
			:return: power: float Comma-separated list of power results The value in the middle of the result array corresponds to the center frequency. The test point separation between two results depends on the resolution bandwidth, see table below. If there is no result for a frequency because no limit is defined, INV is returned. Unit: dBm"""
		rbw_cmd_val = self._cmd_group.get_repcap_cmd_value(rbw, repcap.Rbw)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:SEMask:RBW{rbw_cmd_val}:AVERage?', suppressed)
		return response
