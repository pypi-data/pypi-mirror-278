from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Rbw: enums.RbwB: K030 | K100 | K400 | M1 | PC1 | PC2 Used resolution bandwidth (configured via limit settings) . K030: 30 kHz K100: 100 kHz K400: 400 kHz M1: 1 MHz PC1: 1 % of channel BW PC2: 2 % of channel BW
			- Frequency: List[float]: float Comma-separated list of frequency values Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Rbw', enums.RbwB),
			ArgStruct('Frequency', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Rbw: enums.RbwB = None
			self.Frequency: List[float] = None

	def fetch(self, area=repcap.Area.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:SEMask:AREA<area>:NEGative:FREQuency \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.trace.seMask.area.negative.frequency.fetch(area = repcap.Area.Default) \n
		Returns the frequencies of a single spectrum emission mask area. The area is located below (NEGative) or above (POSitive)
		the carrier center frequency. At the returned frequencies, the power values are measured, see method RsCmwNrFr1Meas.
		NrSubMeas.MultiEval.Trace.SeMask.Area.Positive.Current.fetch. \n
			:param area: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		area_cmd_val = self._cmd_group.get_repcap_cmd_value(area, repcap.Area)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:TRACe:SEMask:AREA{area_cmd_val}:NEGative:FREQuency?', self.__class__.FetchStruct())
