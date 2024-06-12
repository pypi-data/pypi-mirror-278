from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ActLimitCls:
	"""ActLimit commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("actLimit", core, parent)

	# noinspection PyTypeChecker
	def get_endc(self) -> enums.MevLimit:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:ACTLimit:ENDC \n
		Snippet: value: enums.MevLimit = driver.configure.nrSubMeas.multiEval.limit.seMask.actLimit.get_endc() \n
		Selects the active spectrum emission mask and OBW limit for EN-DC. \n
			:return: limit: STD | UDEF STD: use standard limits UDEF: use user-defined limits
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:ACTLimit:ENDC?')
		return Conversions.str_to_scalar_enum(response, enums.MevLimit)

	def set_endc(self, limit: enums.MevLimit) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:ACTLimit:ENDC \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.actLimit.set_endc(limit = enums.MevLimit.STD) \n
		Selects the active spectrum emission mask and OBW limit for EN-DC. \n
			:param limit: STD | UDEF STD: use standard limits UDEF: use user-defined limits
		"""
		param = Conversions.enum_scalar_to_str(limit, enums.MevLimit)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:ACTLimit:ENDC {param}')

	# noinspection PyTypeChecker
	def get_caggregation(self) -> enums.MevLimit:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:ACTLimit:CAGGregation \n
		Snippet: value: enums.MevLimit = driver.configure.nrSubMeas.multiEval.limit.seMask.actLimit.get_caggregation() \n
		Selects the active spectrum emission mask and OBW limit for NR SA with carrier aggregation. \n
			:return: limit: STD | UDEF STD: use standard limits UDEF: use user-defined limits
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:ACTLimit:CAGGregation?')
		return Conversions.str_to_scalar_enum(response, enums.MevLimit)

	def set_caggregation(self, limit: enums.MevLimit) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:ACTLimit:CAGGregation \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.actLimit.set_caggregation(limit = enums.MevLimit.STD) \n
		Selects the active spectrum emission mask and OBW limit for NR SA with carrier aggregation. \n
			:param limit: STD | UDEF STD: use standard limits UDEF: use user-defined limits
		"""
		param = Conversions.enum_scalar_to_str(limit, enums.MevLimit)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:ACTLimit:CAGGregation {param}')
