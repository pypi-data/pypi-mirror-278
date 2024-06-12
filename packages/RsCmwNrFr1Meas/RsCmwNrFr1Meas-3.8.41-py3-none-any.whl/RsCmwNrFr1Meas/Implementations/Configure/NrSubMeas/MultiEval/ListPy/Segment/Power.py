from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerCls:
	"""Power commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	def set(self, power_statistics: int, power_tx_enable: bool, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:POWer \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.segment.power.set(power_statistics = 1, power_tx_enable = False, sEGMent = repcap.SEGMent.Default) \n
		Defines settings for the measurement of the total TX power for segment <no>. \n
			:param power_statistics: integer Statistical length in subframes Range: 1 to 1000
			:param power_tx_enable: OFF | ON Enables or disables the measurement of the total TX power.
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('power_statistics', power_statistics, DataType.Integer), ArgSingle('power_tx_enable', power_tx_enable, DataType.Boolean))
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:POWer {param}'.rstrip())

	# noinspection PyTypeChecker
	class PowerStruct(StructBase):
		"""Response structure. Fields: \n
			- Power_Statistics: int: integer Statistical length in subframes Range: 1 to 1000
			- Power_Tx_Enable: bool: OFF | ON Enables or disables the measurement of the total TX power."""
		__meta_args_list = [
			ArgStruct.scalar_int('Power_Statistics'),
			ArgStruct.scalar_bool('Power_Tx_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Power_Statistics: int = None
			self.Power_Tx_Enable: bool = None

	def get(self, sEGMent=repcap.SEGMent.Default) -> PowerStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:POWer \n
		Snippet: value: PowerStruct = driver.configure.nrSubMeas.multiEval.listPy.segment.power.get(sEGMent = repcap.SEGMent.Default) \n
		Defines settings for the measurement of the total TX power for segment <no>. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for PowerStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:POWer?', self.__class__.PowerStruct())
