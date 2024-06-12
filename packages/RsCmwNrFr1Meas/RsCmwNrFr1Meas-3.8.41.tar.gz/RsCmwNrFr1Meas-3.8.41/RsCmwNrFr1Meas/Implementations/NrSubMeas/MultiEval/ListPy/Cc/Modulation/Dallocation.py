from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DallocationCls:
	"""Dallocation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dallocation", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Nr_Res_Blocks: List[int]: decimal Number of allocated resource blocks
			- Offset_Res_Blocks: List[int]: decimal Offset of the first allocated resource block from the edge of the allocated UL transmission bandwidth"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct('Nr_Res_Blocks', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Offset_Res_Blocks', DataType.IntegerList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Nr_Res_Blocks: List[int] = None
			self.Offset_Res_Blocks: List[int] = None

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST[:CC<Carrier>]:MODulation:DALLocation \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.listPy.cc.modulation.dallocation.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return the detected allocation for all measured list mode segments. The result is determined from the last measured slot
		of the statistical length of a segment. The results are returned as pairs per segment: <Reliability>, {<NrResBlocks>,
		<OffsetResBlocks>}seg 1, {<NrResBlocks>, <OffsetResBlocks>}seg 2, ... \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:CC{carrierComponent_cmd_val}:MODulation:DALLocation?', self.__class__.FetchStruct())
