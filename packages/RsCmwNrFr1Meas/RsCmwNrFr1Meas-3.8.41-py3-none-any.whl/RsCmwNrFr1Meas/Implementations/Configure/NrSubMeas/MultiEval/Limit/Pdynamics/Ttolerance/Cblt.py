from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CbltCls:
	"""Cblt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cblt", core, parent)

	def set(self, tt_power_less_3_g: float, tt_power_great_3_g: float) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:TTOLerance:CBLT \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.pdynamics.ttolerance.cblt.set(tt_power_less_3_g = 1.0, tt_power_great_3_g = 1.0) \n
		Defines test tolerances for power dynamics limits, for channel BW up to 40 MHz. \n
			:param tt_power_less_3_g: numeric For carrier center frequencies up to 3 GHz Range: -3 dB to 3 dB, Unit: dB
			:param tt_power_great_3_g: numeric For carrier center frequencies 3 GHz Range: -3 dB to 3 dB, Unit: dB
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('tt_power_less_3_g', tt_power_less_3_g, DataType.Float), ArgSingle('tt_power_great_3_g', tt_power_great_3_g, DataType.Float))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:TTOLerance:CBLT {param}'.rstrip())

	# noinspection PyTypeChecker
	class CbltStruct(StructBase):
		"""Response structure. Fields: \n
			- Tt_Power_Less_3_G: float: numeric For carrier center frequencies up to 3 GHz Range: -3 dB to 3 dB, Unit: dB
			- Tt_Power_Great_3_G: float: numeric For carrier center frequencies 3 GHz Range: -3 dB to 3 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Tt_Power_Less_3_G'),
			ArgStruct.scalar_float('Tt_Power_Great_3_G')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Tt_Power_Less_3_G: float = None
			self.Tt_Power_Great_3_G: float = None

	def get(self) -> CbltStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:TTOLerance:CBLT \n
		Snippet: value: CbltStruct = driver.configure.nrSubMeas.multiEval.limit.pdynamics.ttolerance.cblt.get() \n
		Defines test tolerances for power dynamics limits, for channel BW up to 40 MHz. \n
			:return: structure: for return value, see the help for CbltStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:TTOLerance:CBLT?', self.__class__.CbltStruct())
