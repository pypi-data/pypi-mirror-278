from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CbandwidthCls:
	"""Cbandwidth commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: ChannelBwExt, default value after init: ChannelBwExt.Bw5"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cbandwidth", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channelBwExt_get', 'repcap_channelBwExt_set', repcap.ChannelBwExt.Bw5)

	def repcap_channelBwExt_set(self, channelBwExt: repcap.ChannelBwExt) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ChannelBwExt.Default
		Default value after init: ChannelBwExt.Bw5"""
		self._cmd_group.set_repcap_enum_value(channelBwExt)

	def repcap_channelBwExt_get(self) -> repcap.ChannelBwExt:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, enable: bool, frequency_start: float, frequency_end: float, level: float, rbw: enums.RbwA, area=repcap.Area.Default, channelBwExt=repcap.ChannelBwExt.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:AREA<area>:CBANdwidth<bw> \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.area.cbandwidth.set(enable = False, frequency_start = 1.0, frequency_end = 1.0, level = 1.0, rbw = enums.RbwA.K030, area = repcap.Area.Default, channelBwExt = repcap.ChannelBwExt.Default) \n
		Defines general requirements for the emission mask area number <area> (for NR SA without CA) . The activation state, the
		area borders, an upper limit and the resolution bandwidth must be specified. The emission mask applies to the channel
		bandwidth <bw>. \n
			:param enable: OFF | ON OFF: Disables the check of these requirements. ON: Enables the check of these requirements.
			:param frequency_start: numeric Stop frequency of the area, relative to the edges of the channel bandwidth. Range: 0 MHz to 105 MHz (less, depending on bw) , Unit: Hz
			:param frequency_end: numeric Range: 0 MHz to not documented, Unit: Hz
			:param level: numeric Upper limit for the area Range: -256 dBm to 256 dBm, Unit: dBm
			:param rbw: K030 | PC1 | M1 Resolution bandwidth to be used for the area Only a subset of the values is allowed, depending on bw. K030: 30 kHz PC1: 1 % of channel bandwidth M1: 1 MHz
			:param area: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')
			:param channelBwExt: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Cbandwidth')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('frequency_start', frequency_start, DataType.Float), ArgSingle('frequency_end', frequency_end, DataType.Float), ArgSingle('level', level, DataType.Float), ArgSingle('rbw', rbw, DataType.Enum, enums.RbwA))
		area_cmd_val = self._cmd_group.get_repcap_cmd_value(area, repcap.Area)
		channelBwExt_cmd_val = self._cmd_group.get_repcap_cmd_value(channelBwExt, repcap.ChannelBwExt)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:AREA{area_cmd_val}:CBANdwidth{channelBwExt_cmd_val} {param}'.rstrip())

	# noinspection PyTypeChecker
	class CbandwidthStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON OFF: Disables the check of these requirements. ON: Enables the check of these requirements.
			- Frequency_Start: float: numeric Stop frequency of the area, relative to the edges of the channel bandwidth. Range: 0 MHz to 105 MHz (less, depending on bw) , Unit: Hz
			- Frequency_End: float: numeric Range: 0 MHz to not documented, Unit: Hz
			- Level: float: numeric Upper limit for the area Range: -256 dBm to 256 dBm, Unit: dBm
			- Rbw: enums.RbwA: K030 | PC1 | M1 Resolution bandwidth to be used for the area Only a subset of the values is allowed, depending on bw. K030: 30 kHz PC1: 1 % of channel bandwidth M1: 1 MHz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Frequency_Start'),
			ArgStruct.scalar_float('Frequency_End'),
			ArgStruct.scalar_float('Level'),
			ArgStruct.scalar_enum('Rbw', enums.RbwA)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Frequency_Start: float = None
			self.Frequency_End: float = None
			self.Level: float = None
			self.Rbw: enums.RbwA = None

	def get(self, area=repcap.Area.Default, channelBwExt=repcap.ChannelBwExt.Default) -> CbandwidthStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:AREA<area>:CBANdwidth<bw> \n
		Snippet: value: CbandwidthStruct = driver.configure.nrSubMeas.multiEval.limit.seMask.area.cbandwidth.get(area = repcap.Area.Default, channelBwExt = repcap.ChannelBwExt.Default) \n
		Defines general requirements for the emission mask area number <area> (for NR SA without CA) . The activation state, the
		area borders, an upper limit and the resolution bandwidth must be specified. The emission mask applies to the channel
		bandwidth <bw>. \n
			:param area: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Area')
			:param channelBwExt: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Cbandwidth')
			:return: structure: for return value, see the help for CbandwidthStruct structure arguments."""
		area_cmd_val = self._cmd_group.get_repcap_cmd_value(area, repcap.Area)
		channelBwExt_cmd_val = self._cmd_group.get_repcap_cmd_value(channelBwExt, repcap.ChannelBwExt)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:AREA{area_cmd_val}:CBANdwidth{channelBwExt_cmd_val}?', self.__class__.CbandwidthStruct())

	def clone(self) -> 'CbandwidthCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CbandwidthCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
