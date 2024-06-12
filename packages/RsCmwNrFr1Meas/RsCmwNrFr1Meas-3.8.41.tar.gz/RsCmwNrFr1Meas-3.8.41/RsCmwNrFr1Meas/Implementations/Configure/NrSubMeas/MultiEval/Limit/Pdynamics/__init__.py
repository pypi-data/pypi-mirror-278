from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PdynamicsCls:
	"""Pdynamics commands group definition. 4 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pdynamics", core, parent)

	@property
	def ttolerance(self):
		"""ttolerance commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ttolerance'):
			from .Ttolerance import TtoleranceCls
			self._ttolerance = TtoleranceCls(self._core, self._cmd_group)
		return self._ttolerance

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:ENABle \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.limit.pdynamics.get_enable() \n
		Enables or disables the limit check for the power dynamics measurement. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:ENABle \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.pdynamics.set_enable(enable = False) \n
		Enables or disables the limit check for the power dynamics measurement. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:ENABle {param}')

	def get_off_power(self) -> float:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:OFFPower \n
		Snippet: value: float = driver.configure.nrSubMeas.multiEval.limit.pdynamics.get_off_power() \n
		Defines an upper limit for the OFF power determined with the power dynamics measurement. \n
			:return: power: numeric Range: -256 dBm to 256 dBm, Unit: dBm
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:OFFPower?')
		return Conversions.str_to_float(response)

	def set_off_power(self, power: float) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:OFFPower \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.pdynamics.set_off_power(power = 1.0) \n
		Defines an upper limit for the OFF power determined with the power dynamics measurement. \n
			:param power: numeric Range: -256 dBm to 256 dBm, Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(power)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PDYNamics:OFFPower {param}')

	def clone(self) -> 'PdynamicsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PdynamicsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
