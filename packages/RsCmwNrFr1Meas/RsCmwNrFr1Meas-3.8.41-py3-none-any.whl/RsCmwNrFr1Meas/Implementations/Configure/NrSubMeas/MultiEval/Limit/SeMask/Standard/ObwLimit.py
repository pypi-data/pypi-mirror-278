from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ObwLimitCls:
	"""ObwLimit commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("obwLimit", core, parent)

	def get_endc(self) -> float or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:OBWLimit:ENDC \n
		Snippet: value: float or bool = driver.configure.nrSubMeas.multiEval.limit.seMask.standard.obwLimit.get_endc() \n
		Configures the activation state of the standard OBW limit, for EN-DC measurements. \n
			:return: obw_limit: (float or boolean) numeric | ON | OFF A setting allows only ON | OFF. A query returns the limit value instead of ON (numeric | OFF) . Range: 10 MHz to 120 MHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:OBWLimit:ENDC?')
		return Conversions.str_to_float_or_bool(response)

	def set_endc(self, obw_limit: float or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:OBWLimit:ENDC \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.standard.obwLimit.set_endc(obw_limit = 1.0) \n
		Configures the activation state of the standard OBW limit, for EN-DC measurements. \n
			:param obw_limit: (float or boolean) numeric | ON | OFF A setting allows only ON | OFF. A query returns the limit value instead of ON (numeric | OFF) . Range: 10 MHz to 120 MHz, Unit: Hz
		"""
		param = Conversions.decimal_or_bool_value_to_str(obw_limit)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:OBWLimit:ENDC {param}')

	def get_caggregation(self) -> float or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:OBWLimit:CAGGregation \n
		Snippet: value: float or bool = driver.configure.nrSubMeas.multiEval.limit.seMask.standard.obwLimit.get_caggregation() \n
		Configures the activation state of the standard OBW limit, for carrier aggregation measurements. \n
			:return: obw_limit: (float or boolean) numeric | ON | OFF A setting allows only ON | OFF. A query returns the limit value instead of ON (numeric | OFF) . Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:OBWLimit:CAGGregation?')
		return Conversions.str_to_float_or_bool(response)

	def set_caggregation(self, obw_limit: float or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:OBWLimit:CAGGregation \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.standard.obwLimit.set_caggregation(obw_limit = 1.0) \n
		Configures the activation state of the standard OBW limit, for carrier aggregation measurements. \n
			:param obw_limit: (float or boolean) numeric | ON | OFF A setting allows only ON | OFF. A query returns the limit value instead of ON (numeric | OFF) . Unit: Hz
		"""
		param = Conversions.decimal_or_bool_value_to_str(obw_limit)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:STANdard:OBWLimit:CAGGregation {param}')
