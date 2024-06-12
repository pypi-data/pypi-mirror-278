from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TrackingCls:
	"""Tracking commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tracking", core, parent)

	def get_phase(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:PHASe \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.modulation.tracking.get_phase() \n
		Activate or deactivate phase tracking. With enabled tracking, fluctuations are compensated. \n
			:return: phase: OFF | ON OFF: Tracking disabled ON: Tracking enabled
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:PHASe?')
		return Conversions.str_to_bool(response)

	def set_phase(self, phase: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:PHASe \n
		Snippet: driver.configure.nrSubMeas.multiEval.modulation.tracking.set_phase(phase = False) \n
		Activate or deactivate phase tracking. With enabled tracking, fluctuations are compensated. \n
			:param phase: OFF | ON OFF: Tracking disabled ON: Tracking enabled
		"""
		param = Conversions.bool_to_str(phase)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:PHASe {param}')

	def get_timing(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:TIMing \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.modulation.tracking.get_timing() \n
		Activate or deactivate timing tracking. With enabled tracking, fluctuations are compensated. \n
			:return: timing: OFF | ON OFF: Tracking disabled ON: Tracking enabled
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:TIMing?')
		return Conversions.str_to_bool(response)

	def set_timing(self, timing: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:TIMing \n
		Snippet: driver.configure.nrSubMeas.multiEval.modulation.tracking.set_timing(timing = False) \n
		Activate or deactivate timing tracking. With enabled tracking, fluctuations are compensated. \n
			:param timing: OFF | ON OFF: Tracking disabled ON: Tracking enabled
		"""
		param = Conversions.bool_to_str(timing)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:TIMing {param}')

	def get_level(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:LEVel \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.modulation.tracking.get_level() \n
		Activate or deactivate level tracking. With enabled tracking, fluctuations are compensated. \n
			:return: level: OFF | ON OFF: Tracking disabled ON: Tracking enabled
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:LEVel?')
		return Conversions.str_to_bool(response)

	def set_level(self, level: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:LEVel \n
		Snippet: driver.configure.nrSubMeas.multiEval.modulation.tracking.set_level(level = False) \n
		Activate or deactivate level tracking. With enabled tracking, fluctuations are compensated. \n
			:param level: OFF | ON OFF: Tracking disabled ON: Tracking enabled
		"""
		param = Conversions.bool_to_str(level)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:TRACking:LEVel {param}')
