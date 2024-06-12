from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdditionalCls:
	"""Additional commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("additional", core, parent)

	def set(self, dmrs_length: int, antenna_port: int = None, carrierComponent=repcap.CarrierComponent.Default, allocation=repcap.Allocation.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:ALLocation<Allocation>:PUSCh:ADDitional \n
		Snippet: driver.configure.nrSubMeas.cc.allocation.pusch.additional.set(dmrs_length = 1, antenna_port = 1, carrierComponent = repcap.CarrierComponent.Default, allocation = repcap.Allocation.Default) \n
		Configures special PUSCH settings, for carrier <no>, allocation <a>. \n
			:param dmrs_length: numeric Length of the DM-RS in symbols. The maximum value is limited by the 'maxLength' setting for the bandwidth part. Range: 1 to 1
			:param antenna_port: numeric Antenna port of the DM-RS.
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param allocation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Allocation')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('dmrs_length', dmrs_length, DataType.Integer), ArgSingle('antenna_port', antenna_port, DataType.Integer, None, is_optional=True))
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		allocation_cmd_val = self._cmd_group.get_repcap_cmd_value(allocation, repcap.Allocation)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:ALLocation{allocation_cmd_val}:PUSCh:ADDitional {param}'.rstrip())

	# noinspection PyTypeChecker
	class AdditionalStruct(StructBase):
		"""Response structure. Fields: \n
			- Dmrs_Length: int: numeric Length of the DM-RS in symbols. The maximum value is limited by the 'maxLength' setting for the bandwidth part. Range: 1 to 1
			- Antenna_Port: int: numeric Antenna port of the DM-RS."""
		__meta_args_list = [
			ArgStruct.scalar_int('Dmrs_Length'),
			ArgStruct.scalar_int('Antenna_Port')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dmrs_Length: int = None
			self.Antenna_Port: int = None

	def get(self, carrierComponent=repcap.CarrierComponent.Default, allocation=repcap.Allocation.Default) -> AdditionalStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:ALLocation<Allocation>:PUSCh:ADDitional \n
		Snippet: value: AdditionalStruct = driver.configure.nrSubMeas.cc.allocation.pusch.additional.get(carrierComponent = repcap.CarrierComponent.Default, allocation = repcap.Allocation.Default) \n
		Configures special PUSCH settings, for carrier <no>, allocation <a>. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:param allocation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Allocation')
			:return: structure: for return value, see the help for AdditionalStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		allocation_cmd_val = self._cmd_group.get_repcap_cmd_value(allocation, repcap.Allocation)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:ALLocation{allocation_cmd_val}:PUSCh:ADDitional?', self.__class__.AdditionalStruct())
