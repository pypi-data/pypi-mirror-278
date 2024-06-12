from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PlcIdCls:
	"""PlcId commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("plcId", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ParameterSetMode:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:PLCid:MODE \n
		Snippet: value: enums.ParameterSetMode = driver.configure.nrSubMeas.listPy.plcId.get_mode() \n
		Selects which physical cell ID setting is used for list mode measurements. \n
			:return: mode: GLOBal | LIST GLOBal The global setting is used for all segments, see method RsCmwNrFr1Meas.Configure.NrSubMeas.Cc.PlcId.set. LIST The cell ID is configured per segment, see method RsCmwNrFr1Meas.Configure.NrSubMeas.ListPy.Segment.Cc.PlcId.set.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:LIST:PLCid:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ParameterSetMode)

	def set_mode(self, mode: enums.ParameterSetMode) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:PLCid:MODE \n
		Snippet: driver.configure.nrSubMeas.listPy.plcId.set_mode(mode = enums.ParameterSetMode.GLOBal) \n
		Selects which physical cell ID setting is used for list mode measurements. \n
			:param mode: GLOBal | LIST GLOBal The global setting is used for all segments, see method RsCmwNrFr1Meas.Configure.NrSubMeas.Cc.PlcId.set. LIST The cell ID is configured per segment, see method RsCmwNrFr1Meas.Configure.NrSubMeas.ListPy.Segment.Cc.PlcId.set.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ParameterSetMode)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:LIST:PLCid:MODE {param}')
