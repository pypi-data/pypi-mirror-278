from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AeoPowerCls:
	"""AeoPower commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("aeoPower", core, parent)

	def get_leading(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LEADing \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.pdynamics.aeoPower.get_leading() \n
		No command help available \n
			:return: leading: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LEADing?')
		return Conversions.str_to_int(response)

	def set_leading(self, leading: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LEADing \n
		Snippet: driver.configure.nrSubMeas.multiEval.pdynamics.aeoPower.set_leading(leading = 1) \n
		No command help available \n
			:param leading: No help available
		"""
		param = Conversions.decimal_value_to_str(leading)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LEADing {param}')

	def get_lagging(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LAGGing \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.pdynamics.aeoPower.get_lagging() \n
		No command help available \n
			:return: lagging: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LAGGing?')
		return Conversions.str_to_int(response)

	def set_lagging(self, lagging: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LAGGing \n
		Snippet: driver.configure.nrSubMeas.multiEval.pdynamics.aeoPower.set_lagging(lagging = 1) \n
		No command help available \n
			:param lagging: No help available
		"""
		param = Conversions.decimal_value_to_str(lagging)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:PDYNamics:AEOPower:LAGGing {param}')
