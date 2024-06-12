from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PcompCls:
	"""Pcomp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pcomp", core, parent)

	def set(self, phase_comp: enums.PhaseComp, user_def_freq: float or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PCOMp \n
		Snippet: driver.configure.nrSubMeas.multiEval.pcomp.set(phase_comp = enums.PhaseComp.CAF, user_def_freq = 1.0) \n
		Specifies the phase compensation applied by the UE during the modulation and upconversion. \n
			:param phase_comp: OFF | CAF | UDEF OFF: no phase compensation CAF: phase compensation for carrier frequency UDEF: phase compensation for frequency UserDefFreq
			:param user_def_freq: (float or boolean) numeric Frequency for PhaseComp = UDEF Range: 0 Hz to 10 GHz, Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('phase_comp', phase_comp, DataType.Enum, enums.PhaseComp), ArgSingle('user_def_freq', user_def_freq, DataType.FloatExt))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:PCOMp {param}'.rstrip())

	# noinspection PyTypeChecker
	class PcompStruct(StructBase):
		"""Response structure. Fields: \n
			- Phase_Comp: enums.PhaseComp: OFF | CAF | UDEF OFF: no phase compensation CAF: phase compensation for carrier frequency UDEF: phase compensation for frequency UserDefFreq
			- User_Def_Freq: float or bool: numeric Frequency for PhaseComp = UDEF Range: 0 Hz to 10 GHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Phase_Comp', enums.PhaseComp),
			ArgStruct.scalar_float_ext('User_Def_Freq')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Phase_Comp: enums.PhaseComp = None
			self.User_Def_Freq: float or bool = None

	def get(self) -> PcompStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PCOMp \n
		Snippet: value: PcompStruct = driver.configure.nrSubMeas.multiEval.pcomp.get() \n
		Specifies the phase compensation applied by the UE during the modulation and upconversion. \n
			:return: structure: for return value, see the help for PcompStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:PCOMp?', self.__class__.PcompStruct())
