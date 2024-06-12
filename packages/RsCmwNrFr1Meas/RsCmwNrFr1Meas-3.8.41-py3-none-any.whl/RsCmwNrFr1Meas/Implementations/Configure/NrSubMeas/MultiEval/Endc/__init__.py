from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EndcCls:
	"""Endc commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("endc", core, parent)

	@property
	def eutra(self):
		"""eutra commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eutra'):
			from .Eutra import EutraCls
			self._eutra = EutraCls(self._core, self._cmd_group)
		return self._eutra

	def get_value(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:ENDC \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.endc.get_value() \n
		Enables or disables the EN-DC mode of the measurement. \n
			:return: on_off: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:ENDC?')
		return Conversions.str_to_bool(response)

	def set_value(self, on_off: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:ENDC \n
		Snippet: driver.configure.nrSubMeas.multiEval.endc.set_value(on_off = False) \n
		Enables or disables the EN-DC mode of the measurement. \n
			:param on_off: OFF | ON
		"""
		param = Conversions.bool_to_str(on_off)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:ENDC {param}')

	def clone(self) -> 'EndcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EndcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
