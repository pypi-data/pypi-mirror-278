from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Utra_2_Neg: float: float ACLR for the second UTRA channel with lower frequency Unit: dB
			- Utra_1_Neg: float: float ACLR for the first UTRA channel with lower frequency Unit: dB
			- Nr_Neg: float: float ACLR for the first NR channel with lower frequency Unit: dB
			- Carrier: float: float Power in the allocated NR channel Unit: dBm
			- Nr_Pos: float: float ACLR for the first NR channel with higher frequency Unit: dB
			- Utra_1_Pos: float: float ACLR for the first UTRA channel with higher frequency Unit: dB
			- Utra_2_Pos: float: float ACLR for the second UTRA channel with higher frequency Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Utra_2_Neg'),
			ArgStruct.scalar_float('Utra_1_Neg'),
			ArgStruct.scalar_float('Nr_Neg'),
			ArgStruct.scalar_float('Carrier'),
			ArgStruct.scalar_float('Nr_Pos'),
			ArgStruct.scalar_float('Utra_1_Pos'),
			ArgStruct.scalar_float('Utra_2_Pos')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Utra_2_Neg: float = None
			self.Utra_1_Neg: float = None
			self.Nr_Neg: float = None
			self.Carrier: float = None
			self.Nr_Pos: float = None
			self.Utra_1_Pos: float = None
			self.Utra_2_Pos: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation:ACLR:CURRent \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.aclr.current.read() \n
		Returns the relative ACLR values for NR standalone, as displayed in the table below the ACLR diagram. The current and
		average values can be retrieved. See also 'View Spectrum ACLR'. The values described below are returned by FETCh and READ
		commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:NRSub:MEASurement<Instance>:MEValuation:ACLR:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:ACLR:CURRent \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.aclr.current.fetch() \n
		Returns the relative ACLR values for NR standalone, as displayed in the table below the ACLR diagram. The current and
		average values can be retrieved. See also 'View Spectrum ACLR'. The values described below are returned by FETCh and READ
		commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:ACLR:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Utra_2_Neg: enums.ResultStatus2: float ACLR for the second UTRA channel with lower frequency Unit: dB
			- Utra_1_Neg: enums.ResultStatus2: float ACLR for the first UTRA channel with lower frequency Unit: dB
			- Nr_Neg: enums.ResultStatus2: float ACLR for the first NR channel with lower frequency Unit: dB
			- Carrier: enums.ResultStatus2: float Power in the allocated NR channel Unit: dBm
			- Nr_Pos: enums.ResultStatus2: float ACLR for the first NR channel with higher frequency Unit: dB
			- Utra_1_Pos: enums.ResultStatus2: float ACLR for the first UTRA channel with higher frequency Unit: dB
			- Utra_2_Pos: enums.ResultStatus2: float ACLR for the second UTRA channel with higher frequency Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Utra_2_Neg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Utra_1_Neg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Nr_Neg', enums.ResultStatus2),
			ArgStruct.scalar_enum('Carrier', enums.ResultStatus2),
			ArgStruct.scalar_enum('Nr_Pos', enums.ResultStatus2),
			ArgStruct.scalar_enum('Utra_1_Pos', enums.ResultStatus2),
			ArgStruct.scalar_enum('Utra_2_Pos', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Utra_2_Neg: enums.ResultStatus2 = None
			self.Utra_1_Neg: enums.ResultStatus2 = None
			self.Nr_Neg: enums.ResultStatus2 = None
			self.Carrier: enums.ResultStatus2 = None
			self.Nr_Pos: enums.ResultStatus2 = None
			self.Utra_1_Pos: enums.ResultStatus2 = None
			self.Utra_2_Pos: enums.ResultStatus2 = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:ACLR:CURRent \n
		Snippet: value: CalculateStruct = driver.nrSubMeas.multiEval.aclr.current.calculate() \n
		Returns the relative ACLR values for NR standalone, as displayed in the table below the ACLR diagram. The current and
		average values can be retrieved. See also 'View Spectrum ACLR'. The values described below are returned by FETCh and READ
		commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:ACLR:CURRent?', self.__class__.CalculateStruct())
