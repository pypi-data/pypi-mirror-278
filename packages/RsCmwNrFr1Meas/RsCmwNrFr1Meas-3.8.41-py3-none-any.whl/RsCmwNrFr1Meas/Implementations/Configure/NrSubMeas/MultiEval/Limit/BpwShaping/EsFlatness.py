from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EsFlatnessCls:
	"""EsFlatness commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("esFlatness", core, parent)

	def set(self, enable: bool, range_1: float, range_2: float) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:BPWShaping:ESFLatness \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.bpwShaping.esFlatness.set(enable = False, range_1 = 1.0, range_2 = 1.0) \n
		Defines limits for the equalizer spectrum flatness (Pi/2-BPSK modulation with shaping) . \n
			:param enable: OFF | ON OFF: disables the limit check ON: enables the limit check
			:param range_1: numeric Upper limit for max(range 1) - min(range 1) Range: -256 dBpp to 256 dBpp, Unit: dBpp
			:param range_2: numeric Upper limit for max(range 2) - min(range 2) Range: -256 dBpp to 256 dBpp, Unit: dBpp
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('range_1', range_1, DataType.Float), ArgSingle('range_2', range_2, DataType.Float))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:BPWShaping:ESFLatness {param}'.rstrip())

	# noinspection PyTypeChecker
	class EsFlatnessStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON OFF: disables the limit check ON: enables the limit check
			- Range_1: float: numeric Upper limit for max(range 1) - min(range 1) Range: -256 dBpp to 256 dBpp, Unit: dBpp
			- Range_2: float: numeric Upper limit for max(range 2) - min(range 2) Range: -256 dBpp to 256 dBpp, Unit: dBpp"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Range_1'),
			ArgStruct.scalar_float('Range_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Range_1: float = None
			self.Range_2: float = None

	def get(self) -> EsFlatnessStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:BPWShaping:ESFLatness \n
		Snippet: value: EsFlatnessStruct = driver.configure.nrSubMeas.multiEval.limit.bpwShaping.esFlatness.get() \n
		Defines limits for the equalizer spectrum flatness (Pi/2-BPSK modulation with shaping) . \n
			:return: structure: for return value, see the help for EsFlatnessStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:BPWShaping:ESFLatness?', self.__class__.EsFlatnessStruct())
