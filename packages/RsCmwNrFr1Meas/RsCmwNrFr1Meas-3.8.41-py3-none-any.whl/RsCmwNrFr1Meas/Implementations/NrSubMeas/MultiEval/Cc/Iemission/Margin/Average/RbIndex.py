from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbIndexCls:
	"""RbIndex commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rbIndex", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tolerance: int: decimal Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits. Unit: %
			- Rb_Index: int: decimal Resource block index for the general margin (at non-allocated RBs)
			- Iq_Image: int: decimal Resource block index for the IQ image margin (at image frequencies of allocated RBs)
			- Carr_Leakage: int: decimal Resource block index for the carrier leakage margin (at carrier frequency)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_int('Rb_Index'),
			ArgStruct.scalar_int('Iq_Image'),
			ArgStruct.scalar_int('Carr_Leakage')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Rb_Index: int = None
			self.Iq_Image: int = None
			self.Carr_Leakage: int = None

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation[:CC<no>]:IEMission:MARGin:AVERage:RBINdex \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.cc.iemission.margin.average.rbIndex.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return resource block indices for inband emission margins, for carrier <no>. At these RB indices, the CURRent, AVERage
		and EXTReme margins have been detected (see method RsCmwNrFr1Meas.NrSubMeas.MultiEval.Cc.Iemission.Margin.Current.fetch
		and ...:AVERage/EXTReme) . \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:IEMission:MARGin:AVERage:RBINdex?', self.__class__.FetchStruct())
