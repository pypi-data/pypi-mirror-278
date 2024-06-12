from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
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

	def set(self, obw_limit: float or bool, channelBwExt=repcap.ChannelBwExt.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:CBANdwidth<bw> \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.obwLimit.cbandwidth.set(obw_limit = 1.0, channelBwExt = repcap.ChannelBwExt.Default) \n
		Defines an upper limit for the occupied bandwidth, depending on the channel bandwidth (for NR SA without CA) . \n
			:param obw_limit: (float or boolean) numeric | ON | OFF Range: 0 MHz to 100 MHz, Unit: Hz ON | OFF enables or disables the limit check.
			:param channelBwExt: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Cbandwidth')
		"""
		param = Conversions.decimal_or_bool_value_to_str(obw_limit)
		channelBwExt_cmd_val = self._cmd_group.get_repcap_cmd_value(channelBwExt, repcap.ChannelBwExt)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:CBANdwidth{channelBwExt_cmd_val} {param}')

	def get(self, channelBwExt=repcap.ChannelBwExt.Default) -> float or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:CBANdwidth<bw> \n
		Snippet: value: float or bool = driver.configure.nrSubMeas.multiEval.limit.seMask.obwLimit.cbandwidth.get(channelBwExt = repcap.ChannelBwExt.Default) \n
		Defines an upper limit for the occupied bandwidth, depending on the channel bandwidth (for NR SA without CA) . \n
			:param channelBwExt: optional repeated capability selector. Default value: Bw5 (settable in the interface 'Cbandwidth')
			:return: obw_limit: (float or boolean) numeric | ON | OFF Range: 0 MHz to 100 MHz, Unit: Hz ON | OFF enables or disables the limit check."""
		channelBwExt_cmd_val = self._cmd_group.get_repcap_cmd_value(channelBwExt, repcap.ChannelBwExt)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:CBANdwidth{channelBwExt_cmd_val}?')
		return Conversions.str_to_float_or_bool(response)

	def clone(self) -> 'CbandwidthCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CbandwidthCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
