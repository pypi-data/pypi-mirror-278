from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDevCls:
	"""StandardDev commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("standardDev", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tolerance: int: decimal Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits. Unit: %
			- Margin: float: float Margin over all non-allocated RBs (scope of general limit component) Unit: dB
			- Iq_Image: float: float Margin at image frequencies of allocated RBs (scope of IQ image limit component) Unit: dB
			- Carr_Leakage: float: float Margin at the carrier frequency (scope of IQ offset limit component) Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Margin'),
			ArgStruct.scalar_float('Iq_Image'),
			ArgStruct.scalar_float('Carr_Leakage')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Margin: float = None
			self.Iq_Image: float = None
			self.Carr_Leakage: float = None

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation[:CC<no>]:IEMission:MARGin:SDEViation \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.cc.iemission.margin.standardDev.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return the limit line margin results for carrier <no>. The CURRent margin indicates the minimum (vertical) distance
		between the inband emissions limit line and the current trace. A negative result indicates that the limit is exceeded.
		The AVERage, EXTReme and SDEViation values are calculated from the current margins. The margin results cannot be
		displayed at the GUI. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:IEMission:MARGin:SDEViation?', self.__class__.FetchStruct())
