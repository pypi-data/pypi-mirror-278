from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbAllocationCls:
	"""RbAllocation commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rbAllocation", core, parent)

	def get_auto(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:AUTO \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.rbAllocation.get_auto() \n
		No command help available \n
			:return: auto: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, auto: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:AUTO \n
		Snippet: driver.configure.nrSubMeas.multiEval.rbAllocation.set_auto(auto = False) \n
		No command help available \n
			:param auto: No help available
		"""
		param = Conversions.bool_to_str(auto)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:AUTO {param}')

	def get_nrb(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:NRB \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.rbAllocation.get_nrb() \n
		No command help available \n
			:return: no_rb: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:NRB?')
		return Conversions.str_to_int(response)

	def set_nrb(self, no_rb: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:NRB \n
		Snippet: driver.configure.nrSubMeas.multiEval.rbAllocation.set_nrb(no_rb = 1) \n
		No command help available \n
			:param no_rb: No help available
		"""
		param = Conversions.decimal_value_to_str(no_rb)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:NRB {param}')

	def get_srb(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:SRB \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.rbAllocation.get_srb() \n
		No command help available \n
			:return: start_rb: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:SRB?')
		return Conversions.str_to_int(response)

	def set_srb(self, start_rb: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:SRB \n
		Snippet: driver.configure.nrSubMeas.multiEval.rbAllocation.set_srb(start_rb = 1) \n
		No command help available \n
			:param start_rb: No help available
		"""
		param = Conversions.decimal_value_to_str(start_rb)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:RBALlocation:SRB {param}')
