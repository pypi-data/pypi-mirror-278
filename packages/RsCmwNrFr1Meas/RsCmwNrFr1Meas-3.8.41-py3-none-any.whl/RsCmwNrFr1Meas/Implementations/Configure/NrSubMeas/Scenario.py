from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScenarioCls:
	"""Scenario commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scenario", core, parent)

	# noinspection PyTypeChecker
	def get_activate(self) -> enums.Scenario:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:SCENario:ACTivate \n
		Snippet: value: enums.Scenario = driver.configure.nrSubMeas.scenario.get_activate() \n
		No command help available \n
			:return: scenario: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:SCENario:ACTivate?')
		return Conversions.str_to_scalar_enum(response, enums.Scenario)

	def set_activate(self, scenario: enums.Scenario) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:SCENario:ACTivate \n
		Snippet: driver.configure.nrSubMeas.scenario.set_activate(scenario = enums.Scenario.CSPath) \n
		No command help available \n
			:param scenario: No help available
		"""
		param = Conversions.enum_scalar_to_str(scenario, enums.Scenario)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:SCENario:ACTivate {param}')
