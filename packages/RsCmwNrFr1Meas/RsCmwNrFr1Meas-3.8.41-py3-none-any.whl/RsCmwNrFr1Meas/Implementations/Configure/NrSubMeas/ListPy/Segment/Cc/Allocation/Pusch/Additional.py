from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdditionalCls:
	"""Additional commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("additional", core, parent)

	def set(self, dmrs_length: int, antenna_port: int = None, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default, allocation=repcap.Allocation.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>[:CC<cc>]:ALLocation<Allocation>:PUSCh:ADDitional \n
		Snippet: driver.configure.nrSubMeas.listPy.segment.cc.allocation.pusch.additional.set(dmrs_length = 1, antenna_port = 1, sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default, allocation = repcap.Allocation.Default) \n
		Configures special PUSCH settings, for carrier <cc>, allocation <a> in segment <no>. \n
			:param dmrs_length: numeric Length of the DM-RS in symbols. The maximum value is limited by the 'maxLength' setting for the bandwidth part. Range: 1 to 1
			:param antenna_port: numeric Antenna port of the DM-RS. Range: 0 to 1
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param allocation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Allocation')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('dmrs_length', dmrs_length, DataType.Integer), ArgSingle('antenna_port', antenna_port, DataType.Integer, None, is_optional=True))
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		allocation_cmd_val = self._cmd_group.get_repcap_cmd_value(allocation, repcap.Allocation)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:ALLocation{allocation_cmd_val}:PUSCh:ADDitional {param}'.rstrip())

	# noinspection PyTypeChecker
	class AdditionalStruct(StructBase):
		"""Response structure. Fields: \n
			- Dmrs_Length: int: numeric Length of the DM-RS in symbols. The maximum value is limited by the 'maxLength' setting for the bandwidth part. Range: 1 to 1
			- Antenna_Port: int: numeric Antenna port of the DM-RS. Range: 0 to 1"""
		__meta_args_list = [
			ArgStruct.scalar_int('Dmrs_Length'),
			ArgStruct.scalar_int('Antenna_Port')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dmrs_Length: int = None
			self.Antenna_Port: int = None

	def get(self, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default, allocation=repcap.Allocation.Default) -> AdditionalStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>[:CC<cc>]:ALLocation<Allocation>:PUSCh:ADDitional \n
		Snippet: value: AdditionalStruct = driver.configure.nrSubMeas.listPy.segment.cc.allocation.pusch.additional.get(sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default, allocation = repcap.Allocation.Default) \n
		Configures special PUSCH settings, for carrier <cc>, allocation <a> in segment <no>. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param allocation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Allocation')
			:return: structure: for return value, see the help for AdditionalStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		allocation_cmd_val = self._cmd_group.get_repcap_cmd_value(allocation, repcap.Allocation)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:ALLocation{allocation_cmd_val}:PUSCh:ADDitional?', self.__class__.AdditionalStruct())
