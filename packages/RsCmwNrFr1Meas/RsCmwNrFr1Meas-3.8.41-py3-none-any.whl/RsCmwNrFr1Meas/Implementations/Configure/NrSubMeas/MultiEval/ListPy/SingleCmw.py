from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SingleCmwCls:
	"""SingleCmw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("singleCmw", core, parent)

	# noinspection PyTypeChecker
	def get_cmode(self) -> enums.ParameterSetMode:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:CMWS:CMODe \n
		Snippet: value: enums.ParameterSetMode = driver.configure.nrSubMeas.multiEval.listPy.singleCmw.get_cmode() \n
		Specifies how the input connector is selected for list mode measurements. \n
			:return: connector_mode: GLOBal | LIST GLOBal: The same input connector is used for all segments. It is selected in the same way as without list mode, see method RsCmwNrFr1Meas.Route.NrSubMeas.Scenario.Salone.set. LIST: The input connector is configured individually for each segment. See method RsCmwNrFr1Meas.Configure.NrSubMeas.MultiEval.ListPy.Segment.SingleCmw.Connector.set.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:CMWS:CMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ParameterSetMode)

	def set_cmode(self, connector_mode: enums.ParameterSetMode) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:CMWS:CMODe \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.singleCmw.set_cmode(connector_mode = enums.ParameterSetMode.GLOBal) \n
		Specifies how the input connector is selected for list mode measurements. \n
			:param connector_mode: GLOBal | LIST GLOBal: The same input connector is used for all segments. It is selected in the same way as without list mode, see method RsCmwNrFr1Meas.Route.NrSubMeas.Scenario.Salone.set. LIST: The input connector is configured individually for each segment. See method RsCmwNrFr1Meas.Configure.NrSubMeas.MultiEval.ListPy.Segment.SingleCmw.Connector.set.
		"""
		param = Conversions.enum_scalar_to_str(connector_mode, enums.ParameterSetMode)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:CMWS:CMODe {param}')
