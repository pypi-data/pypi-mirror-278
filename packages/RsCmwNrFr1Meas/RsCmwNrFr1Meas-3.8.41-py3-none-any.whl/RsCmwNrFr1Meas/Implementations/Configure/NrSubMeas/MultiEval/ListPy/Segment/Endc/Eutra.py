from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EutraCls:
	"""Eutra commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eutra", core, parent)

	def set(self, channel_bw: enums.ChannelBwidthB, carrier_position: enums.CarrierPosition, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:ENDC:EUTRa \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.segment.endc.eutra.set(channel_bw = enums.ChannelBwidthB.B005, carrier_position = enums.CarrierPosition.LONR, sEGMent = repcap.SEGMent.Default) \n
		Configures LTE settings for the EN-DC mode, for segment <no>. \n
			:param channel_bw: B005 | B010 | B015 | B020 Channel bandwidth in MHz (5 MHz to 20 MHz) .
			:param carrier_position: LONR | RONR Position of LTE carrier left (LONR) or right (RONR) of NR carrier.
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('channel_bw', channel_bw, DataType.Enum, enums.ChannelBwidthB), ArgSingle('carrier_position', carrier_position, DataType.Enum, enums.CarrierPosition))
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:ENDC:EUTRa {param}'.rstrip())

	# noinspection PyTypeChecker
	class EutraStruct(StructBase):
		"""Response structure. Fields: \n
			- Channel_Bw: enums.ChannelBwidthB: B005 | B010 | B015 | B020 Channel bandwidth in MHz (5 MHz to 20 MHz) .
			- Carrier_Position: enums.CarrierPosition: LONR | RONR Position of LTE carrier left (LONR) or right (RONR) of NR carrier."""
		__meta_args_list = [
			ArgStruct.scalar_enum('Channel_Bw', enums.ChannelBwidthB),
			ArgStruct.scalar_enum('Carrier_Position', enums.CarrierPosition)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Channel_Bw: enums.ChannelBwidthB = None
			self.Carrier_Position: enums.CarrierPosition = None

	def get(self, sEGMent=repcap.SEGMent.Default) -> EutraStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:ENDC:EUTRa \n
		Snippet: value: EutraStruct = driver.configure.nrSubMeas.multiEval.listPy.segment.endc.eutra.get(sEGMent = repcap.SEGMent.Default) \n
		Configures LTE settings for the EN-DC mode, for segment <no>. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for EutraStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:ENDC:EUTRa?', self.__class__.EutraStruct())
