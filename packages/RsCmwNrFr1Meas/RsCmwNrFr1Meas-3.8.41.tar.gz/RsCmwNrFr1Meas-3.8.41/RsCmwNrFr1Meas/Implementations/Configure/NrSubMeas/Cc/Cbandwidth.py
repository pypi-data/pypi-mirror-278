from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CbandwidthCls:
	"""Cbandwidth commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cbandwidth", core, parent)

	def set(self, channel_bw: enums.ChannelBwidth, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:CBANdwidth \n
		Snippet: driver.configure.nrSubMeas.cc.cbandwidth.set(channel_bw = enums.ChannelBwidth.B005, carrierComponent = repcap.CarrierComponent.Default) \n
		Specifies the channel bandwidth of carrier <no>. \n
			:param channel_bw: B005 | B010 | B015 | B020 | B025 | B030 | B035 | B040 | B045 | B050 | B060 | B070 | B080 | B090 | B100 Channel bandwidth 5 MHz to 100 MHz (Bxxx = xxx MHz) .
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
		"""
		param = Conversions.enum_scalar_to_str(channel_bw, enums.ChannelBwidth)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:CBANdwidth {param}')

	# noinspection PyTypeChecker
	def get(self, carrierComponent=repcap.CarrierComponent.Default) -> enums.ChannelBwidth:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>[:CC<no>]:CBANdwidth \n
		Snippet: value: enums.ChannelBwidth = driver.configure.nrSubMeas.cc.cbandwidth.get(carrierComponent = repcap.CarrierComponent.Default) \n
		Specifies the channel bandwidth of carrier <no>. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: channel_bw: B005 | B010 | B015 | B020 | B025 | B030 | B035 | B040 | B045 | B050 | B060 | B070 | B080 | B090 | B100 Channel bandwidth 5 MHz to 100 MHz (Bxxx = xxx MHz) ."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:CC{carrierComponent_cmd_val}:CBANdwidth?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelBwidth)
