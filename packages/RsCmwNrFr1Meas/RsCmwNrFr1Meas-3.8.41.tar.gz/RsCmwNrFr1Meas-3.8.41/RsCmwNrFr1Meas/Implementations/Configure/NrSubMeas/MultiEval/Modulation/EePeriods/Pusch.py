from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuschCls:
	"""Pusch commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pusch", core, parent)

	# noinspection PyTypeChecker
	def get_leading(self) -> enums.Leading:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LEADing \n
		Snippet: value: enums.Leading = driver.configure.nrSubMeas.multiEval.modulation.eePeriods.pusch.get_leading() \n
		No command help available \n
			:return: leading: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LEADing?')
		return Conversions.str_to_scalar_enum(response, enums.Leading)

	def set_leading(self, leading: enums.Leading) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LEADing \n
		Snippet: driver.configure.nrSubMeas.multiEval.modulation.eePeriods.pusch.set_leading(leading = enums.Leading.MS25) \n
		No command help available \n
			:param leading: No help available
		"""
		param = Conversions.enum_scalar_to_str(leading, enums.Leading)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LEADing {param}')

	# noinspection PyTypeChecker
	def get_lagging(self) -> enums.Lagging:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LAGGing \n
		Snippet: value: enums.Lagging = driver.configure.nrSubMeas.multiEval.modulation.eePeriods.pusch.get_lagging() \n
		No command help available \n
			:return: lagging: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LAGGing?')
		return Conversions.str_to_scalar_enum(response, enums.Lagging)

	def set_lagging(self, lagging: enums.Lagging) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LAGGing \n
		Snippet: driver.configure.nrSubMeas.multiEval.modulation.eePeriods.pusch.set_lagging(lagging = enums.Lagging.MS05) \n
		No command help available \n
			:param lagging: No help available
		"""
		param = Conversions.enum_scalar_to_str(lagging, enums.Lagging)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MODulation:EEPeriods:PUSCh:LAGGing {param}')
