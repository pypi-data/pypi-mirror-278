from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmrsCls:
	"""Dmrs commands group definition. 5 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmrs", core, parent)

	@property
	def sgeneration(self):
		"""sgeneration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sgeneration'):
			from .Sgeneration import SgenerationCls
			self._sgeneration = SgenerationCls(self._core, self._cmd_group)
		return self._sgeneration

	def get_config_type(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:CONFigtype \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.dmrs.get_config_type() \n
		No command help available \n
			:return: config_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:CONFigtype?')
		return Conversions.str_to_int(response)

	def get_max_length(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:MAXLength \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.dmrs.get_max_length() \n
		No command help available \n
			:return: max_length: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:MAXLength?')
		return Conversions.str_to_int(response)

	def set_max_length(self, max_length: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:MAXLength \n
		Snippet: driver.configure.nrSubMeas.multiEval.dmrs.set_max_length(max_length = 1) \n
		No command help available \n
			:param max_length: No help available
		"""
		param = Conversions.decimal_value_to_str(max_length)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:MAXLength {param}')

	def get_aposition(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:APOSition \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.dmrs.get_aposition() \n
		No command help available \n
			:return: add_position: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:APOSition?')
		return Conversions.str_to_int(response)

	def set_aposition(self, add_position: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:APOSition \n
		Snippet: driver.configure.nrSubMeas.multiEval.dmrs.set_aposition(add_position = 1) \n
		No command help available \n
			:param add_position: No help available
		"""
		param = Conversions.decimal_value_to_str(add_position)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:APOSition {param}')

	def get_lzero(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:LZERo \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.dmrs.get_lzero() \n
		No command help available \n
			:return: lzero: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:LZERo?')
		return Conversions.str_to_int(response)

	def set_lzero(self, lzero: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:LZERo \n
		Snippet: driver.configure.nrSubMeas.multiEval.dmrs.set_lzero(lzero = 1) \n
		No command help available \n
			:param lzero: No help available
		"""
		param = Conversions.decimal_value_to_str(lzero)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMRS:LZERo {param}')

	def clone(self) -> 'DmrsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DmrsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
