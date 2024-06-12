from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InvokeCls:
	"""Invoke commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("invoke", core, parent)

	def set(self, sub_carr_spacing: enums.SubCarrSpacing, channel_bw: enums.ChannelBwidth) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:BWConfig:INVoke \n
		Snippet: driver.configure.nrSubMeas.bwConfig.invoke.set(sub_carr_spacing = enums.SubCarrSpacing.S15K, channel_bw = enums.ChannelBwidth.B005) \n
		No command help available \n
			:param sub_carr_spacing: No help available
			:param channel_bw: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sub_carr_spacing', sub_carr_spacing, DataType.Enum, enums.SubCarrSpacing), ArgSingle('channel_bw', channel_bw, DataType.Enum, enums.ChannelBwidth))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:BWConfig:INVoke {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Sub_Carr_Spacing: enums.SubCarrSpacing: No parameter help available
			- Channel_Bw: enums.ChannelBwidth: No parameter help available
			- Remote_Correct: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Sub_Carr_Spacing', enums.SubCarrSpacing),
			ArgStruct.scalar_enum('Channel_Bw', enums.ChannelBwidth),
			ArgStruct.scalar_bool('Remote_Correct')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sub_Carr_Spacing: enums.SubCarrSpacing = None
			self.Channel_Bw: enums.ChannelBwidth = None
			self.Remote_Correct: bool = None

	def get(self) -> GetStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:BWConfig:INVoke \n
		Snippet: value: GetStruct = driver.configure.nrSubMeas.bwConfig.invoke.get() \n
		No command help available \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:BWConfig:INVoke?', self.__class__.GetStruct())
