from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SgenerationCls:
	"""Sgeneration commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sgeneration", core, parent)

	def set(self, initialization: enums.Generator, dmrs_id: int, nscid: int, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default, allocation=repcap.Allocation.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>[:CC<cc>]:ALLocation<Allocation>:PUSCh:SGENeration \n
		Snippet: driver.configure.nrSubMeas.listPy.segment.cc.allocation.pusch.sgeneration.set(initialization = enums.Generator.DID, dmrs_id = 1, nscid = 1, sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default, allocation = repcap.Allocation.Default) \n
		Configures the initialization of the DM-RS sequence generation, for carrier <cc>, allocation <a> in segment <no>. \n
			:param initialization: PHY | DID PHY: physical cell ID used DID: DMRS ID used
			:param dmrs_id: numeric ID for Initialization = DID. Range: 0 to 65535
			:param nscid: numeric Parameter nSCID. Range: 0 to 1
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param allocation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Allocation')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('initialization', initialization, DataType.Enum, enums.Generator), ArgSingle('dmrs_id', dmrs_id, DataType.Integer), ArgSingle('nscid', nscid, DataType.Integer))
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		allocation_cmd_val = self._cmd_group.get_repcap_cmd_value(allocation, repcap.Allocation)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:ALLocation{allocation_cmd_val}:PUSCh:SGENeration {param}'.rstrip())

	# noinspection PyTypeChecker
	class SgenerationStruct(StructBase):
		"""Response structure. Fields: \n
			- Initialization: enums.Generator: PHY | DID PHY: physical cell ID used DID: DMRS ID used
			- Dmrs_Id: int: numeric ID for Initialization = DID. Range: 0 to 65535
			- Nscid: int: numeric Parameter nSCID. Range: 0 to 1"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Initialization', enums.Generator),
			ArgStruct.scalar_int('Dmrs_Id'),
			ArgStruct.scalar_int('Nscid')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Initialization: enums.Generator = None
			self.Dmrs_Id: int = None
			self.Nscid: int = None

	def get(self, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default, allocation=repcap.Allocation.Default) -> SgenerationStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>[:CC<cc>]:ALLocation<Allocation>:PUSCh:SGENeration \n
		Snippet: value: SgenerationStruct = driver.configure.nrSubMeas.listPy.segment.cc.allocation.pusch.sgeneration.get(sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default, allocation = repcap.Allocation.Default) \n
		Configures the initialization of the DM-RS sequence generation, for carrier <cc>, allocation <a> in segment <no>. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param allocation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Allocation')
			:return: structure: for return value, see the help for SgenerationStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		allocation_cmd_val = self._cmd_group.get_repcap_cmd_value(allocation, repcap.Allocation)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:ALLocation{allocation_cmd_val}:PUSCh:SGENeration?', self.__class__.SgenerationStruct())
