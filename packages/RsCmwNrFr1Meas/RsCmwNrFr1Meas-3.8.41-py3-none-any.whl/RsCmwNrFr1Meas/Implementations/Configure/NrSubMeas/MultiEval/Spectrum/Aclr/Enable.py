from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnableCls:
	"""Enable commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, utra_1: bool, utra_2: bool, nr: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SPECtrum:ACLR:ENABle \n
		Snippet: driver.configure.nrSubMeas.multiEval.spectrum.aclr.enable.set(utra_1 = False, utra_2 = False, nr = False) \n
		Enables or disables the evaluation of the first adjacent UTRA channels, second adjacent UTRA channels and first adjacent
		NR channels. \n
			:param utra_1: OFF | ON
			:param utra_2: OFF | ON
			:param nr: OFF | ON
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('utra_1', utra_1, DataType.Boolean), ArgSingle('utra_2', utra_2, DataType.Boolean), ArgSingle('nr', nr, DataType.Boolean))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:SPECtrum:ACLR:ENABle {param}'.rstrip())

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Response structure. Fields: \n
			- Utra_1: bool: OFF | ON
			- Utra_2: bool: OFF | ON
			- Nr: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Utra_1'),
			ArgStruct.scalar_bool('Utra_2'),
			ArgStruct.scalar_bool('Nr')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Utra_1: bool = None
			self.Utra_2: bool = None
			self.Nr: bool = None

	def get(self) -> EnableStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SPECtrum:ACLR:ENABle \n
		Snippet: value: EnableStruct = driver.configure.nrSubMeas.multiEval.spectrum.aclr.enable.get() \n
		Enables or disables the evaluation of the first adjacent UTRA channels, second adjacent UTRA channels and first adjacent
		NR channels. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:SPECtrum:ACLR:ENABle?', self.__class__.EnableStruct())

	def get_endc(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SPECtrum:ACLR:ENABle:ENDC \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.spectrum.aclr.enable.get_endc() \n
		Enables or disables the evaluation of the adjacent channel power in EN-DC mode. \n
			:return: endc: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:SPECtrum:ACLR:ENABle:ENDC?')
		return Conversions.str_to_bool(response)

	def set_endc(self, endc: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SPECtrum:ACLR:ENABle:ENDC \n
		Snippet: driver.configure.nrSubMeas.multiEval.spectrum.aclr.enable.set_endc(endc = False) \n
		Enables or disables the evaluation of the adjacent channel power in EN-DC mode. \n
			:param endc: OFF | ON
		"""
		param = Conversions.bool_to_str(endc)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:SPECtrum:ACLR:ENABle:ENDC {param}')
