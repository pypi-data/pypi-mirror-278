from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UlDlCls:
	"""UlDl commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ulDl", core, parent)

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	# noinspection PyTypeChecker
	def get_periodicity(self) -> enums.Periodicity:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:ULDL:PERiodicity \n
		Snippet: value: enums.Periodicity = driver.configure.nrSubMeas.ulDl.get_periodicity() \n
		Configures the periodicity of the TDD UL-DL pattern. \n
			:return: periodicity: MS05 | MS1 | MS125 | MS2 | MS25 | MS3 | MS4 | MS5 | MS10 0.5 ms, 1 ms, 1.25 ms, 2 ms, 2.5 ms, 3 ms, 4 ms, 5 ms, 10 ms
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:ULDL:PERiodicity?')
		return Conversions.str_to_scalar_enum(response, enums.Periodicity)

	def set_periodicity(self, periodicity: enums.Periodicity) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:ULDL:PERiodicity \n
		Snippet: driver.configure.nrSubMeas.ulDl.set_periodicity(periodicity = enums.Periodicity.MS05) \n
		Configures the periodicity of the TDD UL-DL pattern. \n
			:param periodicity: MS05 | MS1 | MS125 | MS2 | MS25 | MS3 | MS4 | MS5 | MS10 0.5 ms, 1 ms, 1.25 ms, 2 ms, 2.5 ms, 3 ms, 4 ms, 5 ms, 10 ms
		"""
		param = Conversions.enum_scalar_to_str(periodicity, enums.Periodicity)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:ULDL:PERiodicity {param}')

	def clone(self) -> 'UlDlCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UlDlCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
