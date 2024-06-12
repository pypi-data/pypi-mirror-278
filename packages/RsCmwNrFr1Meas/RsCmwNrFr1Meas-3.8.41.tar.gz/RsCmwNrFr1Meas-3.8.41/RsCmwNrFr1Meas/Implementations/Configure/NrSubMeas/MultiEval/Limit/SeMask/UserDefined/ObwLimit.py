from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ObwLimitCls:
	"""ObwLimit commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("obwLimit", core, parent)

	def get_caggregation(self) -> float or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:UDEFined:OBWLimit:CAGGregation \n
		Snippet: value: float or bool = driver.configure.nrSubMeas.multiEval.limit.seMask.userDefined.obwLimit.get_caggregation() \n
		Defines an upper user-defined limit for the OBW, for carrier aggregation measurements. \n
			:return: obw_limit: (float or boolean) numeric | ON | OFF Range: 10 MHz to 200 MHz, Unit: Hz ON | OFF enables or disables the limit check.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:UDEFined:OBWLimit:CAGGregation?')
		return Conversions.str_to_float_or_bool(response)

	def set_caggregation(self, obw_limit: float or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:UDEFined:OBWLimit:CAGGregation \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.userDefined.obwLimit.set_caggregation(obw_limit = 1.0) \n
		Defines an upper user-defined limit for the OBW, for carrier aggregation measurements. \n
			:param obw_limit: (float or boolean) numeric | ON | OFF Range: 10 MHz to 200 MHz, Unit: Hz ON | OFF enables or disables the limit check.
		"""
		param = Conversions.decimal_or_bool_value_to_str(obw_limit)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:UDEFined:OBWLimit:CAGGregation {param}')
