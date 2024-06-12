from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwPartCls:
	"""BwPart commands group definition. 4 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bwPart", core, parent)

	@property
	def pusch(self):
		"""pusch commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Pusch import PuschCls
			self._pusch = PuschCls(self._core, self._cmd_group)
		return self._pusch

	def set(self, bwp: enums.BandwidthPart, sub_car_spacing: enums.SubCarrSpacing, cyclic_prefix: enums.CyclicPrefix, number_rb: int, start_rb: int, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>[:CC<cc>]:BWPart \n
		Snippet: driver.configure.nrSubMeas.listPy.segment.cc.bwPart.set(bwp = enums.BandwidthPart.BWP0, sub_car_spacing = enums.SubCarrSpacing.S15K, cyclic_prefix = enums.CyclicPrefix.EXTended, number_rb = 1, start_rb = 1, sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Configures basic properties of the <BWP> on carrier <cc> in segment <no>. For dependencies of the RB ranges, see
		'Resource elements, grids and blocks'. \n
			:param bwp: BWP0
			:param sub_car_spacing: S15K | S30K | S60K Subcarrier spacing 15 kHz, 30 kHz, 60 kHz.
			:param cyclic_prefix: NORMal | EXTended EXTended cyclic prefix is only possible for 60-kHz SC spacing.
			:param number_rb: numeric Number of RBs in the bandwidth part. Range: 11 to 273
			:param start_rb: numeric Index of the first RB in the bandwidth part. Range: 0 to 262
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('bwp', bwp, DataType.Enum, enums.BandwidthPart), ArgSingle('sub_car_spacing', sub_car_spacing, DataType.Enum, enums.SubCarrSpacing), ArgSingle('cyclic_prefix', cyclic_prefix, DataType.Enum, enums.CyclicPrefix), ArgSingle('number_rb', number_rb, DataType.Integer), ArgSingle('start_rb', start_rb, DataType.Integer))
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:BWPart {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Sub_Car_Spacing: enums.SubCarrSpacing: S15K | S30K | S60K Subcarrier spacing 15 kHz, 30 kHz, 60 kHz.
			- Cyclic_Prefix: enums.CyclicPrefix: NORMal | EXTended EXTended cyclic prefix is only possible for 60-kHz SC spacing.
			- Number_Rb: int: numeric Number of RBs in the bandwidth part. Range: 11 to 273
			- Start_Rb: int: numeric Index of the first RB in the bandwidth part. Range: 0 to 262"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Sub_Car_Spacing', enums.SubCarrSpacing),
			ArgStruct.scalar_enum('Cyclic_Prefix', enums.CyclicPrefix),
			ArgStruct.scalar_int('Number_Rb'),
			ArgStruct.scalar_int('Start_Rb')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sub_Car_Spacing: enums.SubCarrSpacing = None
			self.Cyclic_Prefix: enums.CyclicPrefix = None
			self.Number_Rb: int = None
			self.Start_Rb: int = None

	def get(self, bwp: enums.BandwidthPart, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default) -> GetStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>[:CC<cc>]:BWPart \n
		Snippet: value: GetStruct = driver.configure.nrSubMeas.listPy.segment.cc.bwPart.get(bwp = enums.BandwidthPart.BWP0, sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Configures basic properties of the <BWP> on carrier <cc> in segment <no>. For dependencies of the RB ranges, see
		'Resource elements, grids and blocks'. \n
			:param bwp: BWP0
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = Conversions.enum_scalar_to_str(bwp, enums.BandwidthPart)
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:BWPart? {param}', self.__class__.GetStruct())

	def clone(self) -> 'BwPartCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BwPartCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
