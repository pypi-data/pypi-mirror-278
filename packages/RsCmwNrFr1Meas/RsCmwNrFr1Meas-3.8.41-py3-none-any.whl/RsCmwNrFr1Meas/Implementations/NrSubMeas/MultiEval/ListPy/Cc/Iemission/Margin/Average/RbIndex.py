from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from ......... import repcap


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
			- Rb_Index: List[int]: decimal Resource block index for the general margin (at non-allocated RBs)
			- Iq_Image: List[int]: decimal Resource block index for the IQ image margin (at image frequencies of allocated RBs)
			- Carr_Leakage: List[int]: decimal Resource block index for the carrier leakage margin (at carrier frequency)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Rb_Index', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Iq_Image', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Carr_Leakage', DataType.IntegerList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Rb_Index: List[int] = None
			self.Iq_Image: List[int] = None
			self.Carr_Leakage: List[int] = None

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:IEMission:MARGin:AVERage:RBINdex \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.listPy.cc.iemission.margin.average.rbIndex.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return resource block indices of the inband emission measurement for all measured list mode segments, for carrier <c>. At
		these RB indices, the CURRent, AVERage and EXTReme margins have been detected. The results are returned as triplets per
		segment: <Reliability>, {<RBindex>, <IQImage>, <CarrLeakage>}seg 1, {<RBindex>, <IQImage>, <CarrLeakage>}seg 2, ... \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:IEMission:MARGin:AVERage:RBINdex?', self.__class__.FetchStruct())
