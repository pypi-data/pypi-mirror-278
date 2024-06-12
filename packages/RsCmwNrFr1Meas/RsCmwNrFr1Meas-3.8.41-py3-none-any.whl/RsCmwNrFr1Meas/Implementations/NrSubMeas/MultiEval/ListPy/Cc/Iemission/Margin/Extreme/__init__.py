from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExtremeCls:
	"""Extreme commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("extreme", core, parent)

	@property
	def rbIndex(self):
		"""rbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbIndex'):
			from .RbIndex import RbIndexCls
			self._rbIndex = RbIndexCls(self._core, self._cmd_group)
		return self._rbIndex

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Margin: List[float]: float Margin over all non-allocated RBs (scope of general limit component) Unit: dB
			- Iq_Image: List[float]: float Margin at image frequencies of allocated RBs (scope of IQ image limit component) Unit: dB
			- Carr_Leakage: List[float]: float Margin at the carrier frequency (scope of IQ offset limit component) Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Margin', DataType.FloatList, None, False, True, 1),
			ArgStruct('Iq_Image', DataType.FloatList, None, False, True, 1),
			ArgStruct('Carr_Leakage', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Margin: List[float] = None
			self.Iq_Image: List[float] = None
			self.Carr_Leakage: List[float] = None

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:IEMission:MARGin:EXTReme \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.listPy.cc.iemission.margin.extreme.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return the inband emission limit line margin results for all measured list mode segments, for carrier <c>. The CURRent
		margins indicate the minimum (vertical) distance between the limit line and the current trace. A negative result
		indicates that the limit is exceeded. The AVERage, EXTReme and SDEViation values are calculated from the current margins.
		The results are returned as triplets per segment: <Reliability>, {<Margin>, <IQImage>, <CarrLeakage>}seg 1, {<Margin>,
		<IQImage>, <CarrLeakage>}seg 2, ... \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:IEMission:MARGin:EXTReme?', self.__class__.FetchStruct())

	def clone(self) -> 'ExtremeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExtremeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
