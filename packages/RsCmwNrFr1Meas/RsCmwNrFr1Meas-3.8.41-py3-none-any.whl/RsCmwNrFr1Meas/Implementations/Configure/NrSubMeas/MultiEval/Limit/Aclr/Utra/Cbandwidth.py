from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........Internal.RepeatedCapability import RepeatedCapability
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

	def set(self, relative_level: float or bool, absolute_level: float or bool, utraChannel=repcap.UtraChannel.Default, channelBwExt=repcap.ChannelBwExt.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:ACLR:UTRA<no>:CBANdwidth<bw> \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.aclr.utra.cbandwidth.set(relative_level = 1.0, absolute_level = 1.0, utraChannel = repcap.UtraChannel.Default, channelBwExt = repcap.ChannelBwExt.Default) \n
		Defines relative and absolute limits for the ACLR measured in the first or second adjacent UTRA channel, depending on
		UTRA<no> (for NR SA without CA) . The settings are defined separately for each channel bandwidth. \n
			:param relative_level: (float or boolean) numeric | ON | OFF Relative lower ACLR limit without test tolerance Range: -256 dB to 256 dB, Unit: dB ON | OFF enables or disables the limit check.
			:param absolute_level: (float or boolean) numeric | ON | OFF Range: -256 dBm to 256 dBm, Unit: dBm ON | OFF enables or disables the limit check.
			:param utraChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utra')
			:param channelBwExt: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Cbandwidth')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('relative_level', relative_level, DataType.FloatExt), ArgSingle('absolute_level', absolute_level, DataType.FloatExt))
		utraChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(utraChannel, repcap.UtraChannel)
		channelBwExt_cmd_val = self._cmd_group.get_repcap_cmd_value(channelBwExt, repcap.ChannelBwExt)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:ACLR:UTRA{utraChannel_cmd_val}:CBANdwidth{channelBwExt_cmd_val} {param}'.rstrip())

	# noinspection PyTypeChecker
	class CbandwidthStruct(StructBase):
		"""Response structure. Fields: \n
			- Relative_Level: float or bool: numeric | ON | OFF Relative lower ACLR limit without test tolerance Range: -256 dB to 256 dB, Unit: dB ON | OFF enables or disables the limit check.
			- Absolute_Level: float or bool: numeric | ON | OFF Range: -256 dBm to 256 dBm, Unit: dBm ON | OFF enables or disables the limit check."""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Relative_Level'),
			ArgStruct.scalar_float_ext('Absolute_Level')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Relative_Level: float or bool = None
			self.Absolute_Level: float or bool = None

	def get(self, utraChannel=repcap.UtraChannel.Default, channelBwExt=repcap.ChannelBwExt.Default) -> CbandwidthStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:ACLR:UTRA<no>:CBANdwidth<bw> \n
		Snippet: value: CbandwidthStruct = driver.configure.nrSubMeas.multiEval.limit.aclr.utra.cbandwidth.get(utraChannel = repcap.UtraChannel.Default, channelBwExt = repcap.ChannelBwExt.Default) \n
		Defines relative and absolute limits for the ACLR measured in the first or second adjacent UTRA channel, depending on
		UTRA<no> (for NR SA without CA) . The settings are defined separately for each channel bandwidth. \n
			:param utraChannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utra')
			:param channelBwExt: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Cbandwidth')
			:return: structure: for return value, see the help for CbandwidthStruct structure arguments."""
		utraChannel_cmd_val = self._cmd_group.get_repcap_cmd_value(utraChannel, repcap.UtraChannel)
		channelBwExt_cmd_val = self._cmd_group.get_repcap_cmd_value(channelBwExt, repcap.ChannelBwExt)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:ACLR:UTRA{utraChannel_cmd_val}:CBANdwidth{channelBwExt_cmd_val}?', self.__class__.CbandwidthStruct())

	def clone(self) -> 'CbandwidthCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CbandwidthCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
