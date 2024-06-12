from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BpwShapingCls:
	"""BpwShaping commands group definition. 8 total commands, 6 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bpwShaping", core, parent)

	@property
	def evMagnitude(self):
		"""evMagnitude commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_evMagnitude'):
			from .EvMagnitude import EvMagnitudeCls
			self._evMagnitude = EvMagnitudeCls(self._core, self._cmd_group)
		return self._evMagnitude

	@property
	def merror(self):
		"""merror commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_merror'):
			from .Merror import MerrorCls
			self._merror = MerrorCls(self._core, self._cmd_group)
		return self._merror

	@property
	def perror(self):
		"""perror commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_perror'):
			from .Perror import PerrorCls
			self._perror = PerrorCls(self._core, self._cmd_group)
		return self._perror

	@property
	def iqOffset(self):
		"""iqOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqOffset'):
			from .IqOffset import IqOffsetCls
			self._iqOffset = IqOffsetCls(self._core, self._cmd_group)
		return self._iqOffset

	@property
	def ibe(self):
		"""ibe commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ibe'):
			from .Ibe import IbeCls
			self._ibe = IbeCls(self._core, self._cmd_group)
		return self._ibe

	@property
	def esFlatness(self):
		"""esFlatness commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_esFlatness'):
			from .EsFlatness import EsFlatnessCls
			self._esFlatness = EsFlatnessCls(self._core, self._cmd_group)
		return self._esFlatness

	def get_freq_error(self) -> float or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:BPWShaping:FERRor \n
		Snippet: value: float or bool = driver.configure.nrSubMeas.multiEval.limit.bpwShaping.get_freq_error() \n
		Defines an upper limit for the carrier frequency error (Pi/2-BPSK modulation with shaping) . \n
			:return: frequency_error: (float or boolean) numeric | ON | OFF Range: 0 ppm to 1 ppm, Unit: ppm ON | OFF enables or disables the limit check.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:BPWShaping:FERRor?')
		return Conversions.str_to_float_or_bool(response)

	def set_freq_error(self, frequency_error: float or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:BPWShaping:FERRor \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.bpwShaping.set_freq_error(frequency_error = 1.0) \n
		Defines an upper limit for the carrier frequency error (Pi/2-BPSK modulation with shaping) . \n
			:param frequency_error: (float or boolean) numeric | ON | OFF Range: 0 ppm to 1 ppm, Unit: ppm ON | OFF enables or disables the limit check.
		"""
		param = Conversions.decimal_or_bool_value_to_str(frequency_error)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:BPWShaping:FERRor {param}')

	def clone(self) -> 'BpwShapingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BpwShapingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
