from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScountCls:
	"""Scount commands group definition. 6 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scount", core, parent)

	@property
	def spectrum(self):
		"""spectrum commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_spectrum'):
			from .Spectrum import SpectrumCls
			self._spectrum = SpectrumCls(self._core, self._cmd_group)
		return self._spectrum

	def get_modulation(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:MODulation \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.scount.get_modulation() \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. \n
			:return: statistic_count: numeric Range: 1 slot to 1000 slots
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:MODulation?')
		return Conversions.str_to_int(response)

	def set_modulation(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:MODulation \n
		Snippet: driver.configure.nrSubMeas.multiEval.scount.set_modulation(statistic_count = 1) \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. \n
			:param statistic_count: numeric Range: 1 slot to 1000 slots
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:MODulation {param}')

	def get_power(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:POWer \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.scount.get_power() \n
		No command help available \n
			:return: statistic_count: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:POWer?')
		return Conversions.str_to_int(response)

	def set_power(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:POWer \n
		Snippet: driver.configure.nrSubMeas.multiEval.scount.set_power(statistic_count = 1) \n
		No command help available \n
			:param statistic_count: No help available
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:POWer {param}')

	def get_pdynamics(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:PDYNamics \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.scount.get_pdynamics() \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. \n
			:return: statistic_count: numeric Number of measurement intervals Range: 1 subframe to 1000 subframes
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:PDYNamics?')
		return Conversions.str_to_int(response)

	def set_pdynamics(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:PDYNamics \n
		Snippet: driver.configure.nrSubMeas.multiEval.scount.set_pdynamics(statistic_count = 1) \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. \n
			:param statistic_count: numeric Number of measurement intervals Range: 1 subframe to 1000 subframes
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:PDYNamics {param}')

	def get_tx_power(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:TXPower \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.scount.get_tx_power() \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. \n
			:return: statistic_count: numeric Number of measurement intervals Range: 1 slot to 1000 slots
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:TXPower?')
		return Conversions.str_to_int(response)

	def set_tx_power(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:TXPower \n
		Snippet: driver.configure.nrSubMeas.multiEval.scount.set_tx_power(statistic_count = 1) \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. \n
			:param statistic_count: numeric Number of measurement intervals Range: 1 slot to 1000 slots
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCOunt:TXPower {param}')

	def clone(self) -> 'ScountCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScountCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
