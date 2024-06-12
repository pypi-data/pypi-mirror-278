from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EvMagnitudeCls:
	"""EvMagnitude commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("evMagnitude", core, parent)

	def set(self, rms: float or bool, peak: float or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:EVMagnitude \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.phbpsk.evMagnitude.set(rms = 1.0, peak = 1.0) \n
		Defines upper limits for the RMS and peak values of the error vector magnitude (EVM) for Pi/2-BPSK. \n
			:param rms: (float or boolean) numeric | ON | OFF Range: 0 % to 100 %, Unit: % ON | OFF enables or disables the limit check.
			:param peak: (float or boolean) numeric | ON | OFF Range: 0 % to 100 %, Unit: % ON | OFF enables or disables the limit check.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('rms', rms, DataType.FloatExt), ArgSingle('peak', peak, DataType.FloatExt))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:EVMagnitude {param}'.rstrip())

	# noinspection PyTypeChecker
	class EvMagnitudeStruct(StructBase):
		"""Response structure. Fields: \n
			- Rms: float or bool: numeric | ON | OFF Range: 0 % to 100 %, Unit: % ON | OFF enables or disables the limit check.
			- Peak: float or bool: numeric | ON | OFF Range: 0 % to 100 %, Unit: % ON | OFF enables or disables the limit check."""
		__meta_args_list = [
			ArgStruct.scalar_float_ext('Rms'),
			ArgStruct.scalar_float_ext('Peak')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rms: float or bool = None
			self.Peak: float or bool = None

	def get(self) -> EvMagnitudeStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:EVMagnitude \n
		Snippet: value: EvMagnitudeStruct = driver.configure.nrSubMeas.multiEval.limit.phbpsk.evMagnitude.get() \n
		Defines upper limits for the RMS and peak values of the error vector magnitude (EVM) for Pi/2-BPSK. \n
			:return: structure: for return value, see the help for EvMagnitudeStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:EVMagnitude?', self.__class__.EvMagnitudeStruct())
