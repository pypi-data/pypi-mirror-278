from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModulationCls:
	"""Modulation commands group definition. 8 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("modulation", core, parent)

	@property
	def tracking(self):
		"""tracking commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_tracking'):
			from .Tracking import TrackingCls
			self._tracking = TrackingCls(self._core, self._cmd_group)
		return self._tracking

	@property
	def ewLength(self):
		"""ewLength commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ewLength'):
			from .EwLength import EwLengthCls
			self._ewLength = EwLengthCls(self._core, self._cmd_group)
		return self._ewLength

	@property
	def eePeriods(self):
		"""eePeriods commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_eePeriods'):
			from .EePeriods import EePeriodsCls
			self._eePeriods = EePeriodsCls(self._core, self._cmd_group)
		return self._eePeriods

	def get_tdl_offset(self) -> float:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TDLoffset \n
		Snippet: value: float = driver.configure.nrSubMeas.multiEval.modulation.get_tdl_offset() \n
		Specifies the offset of the UL DC subcarrier from the center frequency, as number of subcarriers. \n
			:return: offset: numeric Range: -2048 to 2047
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TDLoffset?')
		return Conversions.str_to_float(response)

	def set_tdl_offset(self, offset: float) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TDLoffset \n
		Snippet: driver.configure.nrSubMeas.multiEval.modulation.set_tdl_offset(offset = 1.0) \n
		Specifies the offset of the UL DC subcarrier from the center frequency, as number of subcarriers. \n
			:param offset: numeric Range: -2048 to 2047
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TDLoffset {param}')

	def clone(self) -> 'ModulationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ModulationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
