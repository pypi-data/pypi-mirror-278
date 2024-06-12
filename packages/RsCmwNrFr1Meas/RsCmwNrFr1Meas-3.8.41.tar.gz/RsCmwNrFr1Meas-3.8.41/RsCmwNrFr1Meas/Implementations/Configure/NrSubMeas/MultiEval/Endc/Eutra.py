from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EutraCls:
	"""Eutra commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eutra", core, parent)

	def set(self, channel_bw: enums.ChannelBwidthB, carrier_position: enums.CarrierPosition) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:ENDC:EUTRa \n
		Snippet: driver.configure.nrSubMeas.multiEval.endc.eutra.set(channel_bw = enums.ChannelBwidthB.B005, carrier_position = enums.CarrierPosition.LONR) \n
		Configures LTE settings for EN-DC. \n
			:param channel_bw: B005 | B010 | B015 | B020 Channel bandwidth in MHz (5 MHz to 20 MHz) .
			:param carrier_position: LONR | RONR Position of LTE carrier left (LONR) or right (RONR) of NR carrier.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('channel_bw', channel_bw, DataType.Enum, enums.ChannelBwidthB), ArgSingle('carrier_position', carrier_position, DataType.Enum, enums.CarrierPosition))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:ENDC:EUTRa {param}'.rstrip())

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

	def get(self) -> EutraStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:ENDC:EUTRa \n
		Snippet: value: EutraStruct = driver.configure.nrSubMeas.multiEval.endc.eutra.get() \n
		Configures LTE settings for EN-DC. \n
			:return: structure: for return value, see the help for EutraStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:ENDC:EUTRa?', self.__class__.EutraStruct())
