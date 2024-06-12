from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllocationCls:
	"""Allocation commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("allocation", core, parent)

	def get_nsymbols(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:ALLocation:NSYMbols \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.allocation.get_nsymbols() \n
		No command help available \n
			:return: no_symbols: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:ALLocation:NSYMbols?')
		return Conversions.str_to_int(response)

	def set_nsymbols(self, no_symbols: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:ALLocation:NSYMbols \n
		Snippet: driver.configure.nrSubMeas.multiEval.allocation.set_nsymbols(no_symbols = 1) \n
		No command help available \n
			:param no_symbols: No help available
		"""
		param = Conversions.decimal_value_to_str(no_symbols)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:ALLocation:NSYMbols {param}')

	def get_ssymbol(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:ALLocation:SSYMbol \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.allocation.get_ssymbol() \n
		No command help available \n
			:return: start_symbol: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:ALLocation:SSYMbol?')
		return Conversions.str_to_int(response)

	def set_ssymbol(self, start_symbol: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:ALLocation:SSYMbol \n
		Snippet: driver.configure.nrSubMeas.multiEval.allocation.set_ssymbol(start_symbol = 1) \n
		No command help available \n
			:param start_symbol: No help available
		"""
		param = Conversions.decimal_value_to_str(start_symbol)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:ALLocation:SSYMbol {param}')
