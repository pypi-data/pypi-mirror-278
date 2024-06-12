from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MsubFramesCls:
	"""MsubFrames commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("msubFrames", core, parent)

	def set(self, sub_frame_offset: int, sub_frame_count: int, meas_subframe: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MSUBframes \n
		Snippet: driver.configure.nrSubMeas.multiEval.msubFrames.set(sub_frame_offset = 1, sub_frame_count = 1, meas_subframe = 1) \n
		No command help available \n
			:param sub_frame_offset: No help available
			:param sub_frame_count: No help available
			:param meas_subframe: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sub_frame_offset', sub_frame_offset, DataType.Integer), ArgSingle('sub_frame_count', sub_frame_count, DataType.Integer), ArgSingle('meas_subframe', meas_subframe, DataType.Integer))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MSUBframes {param}'.rstrip())

	# noinspection PyTypeChecker
	class MsubFramesStruct(StructBase):
		"""Response structure. Fields: \n
			- Sub_Frame_Offset: int: No parameter help available
			- Sub_Frame_Count: int: No parameter help available
			- Meas_Subframe: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Sub_Frame_Offset'),
			ArgStruct.scalar_int('Sub_Frame_Count'),
			ArgStruct.scalar_int('Meas_Subframe')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sub_Frame_Offset: int = None
			self.Sub_Frame_Count: int = None
			self.Meas_Subframe: int = None

	def get(self) -> MsubFramesStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MSUBframes \n
		Snippet: value: MsubFramesStruct = driver.configure.nrSubMeas.multiEval.msubFrames.get() \n
		No command help available \n
			:return: structure: for return value, see the help for MsubFramesStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MSUBframes?', self.__class__.MsubFramesStruct())
