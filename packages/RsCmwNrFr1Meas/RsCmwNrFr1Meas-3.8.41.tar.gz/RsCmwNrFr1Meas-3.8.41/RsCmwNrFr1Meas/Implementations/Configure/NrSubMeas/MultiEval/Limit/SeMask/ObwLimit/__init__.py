from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ObwLimitCls:
	"""ObwLimit commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("obwLimit", core, parent)

	@property
	def cbandwidth(self):
		"""cbandwidth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbandwidth'):
			from .Cbandwidth import CbandwidthCls
			self._cbandwidth = CbandwidthCls(self._core, self._cmd_group)
		return self._cbandwidth

	def get_endc(self) -> float or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:ENDC \n
		Snippet: value: float or bool = driver.configure.nrSubMeas.multiEval.limit.seMask.obwLimit.get_endc() \n
		Defines an upper user-defined limit for the OBW, for EN-DC measurements. \n
			:return: obw_limit: (float or boolean) numeric | ON | OFF Range: 10 MHz to 120 MHz, Unit: Hz ON | OFF enables or disables the limit check.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:ENDC?')
		return Conversions.str_to_float_or_bool(response)

	def set_endc(self, obw_limit: float or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:ENDC \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.seMask.obwLimit.set_endc(obw_limit = 1.0) \n
		Defines an upper user-defined limit for the OBW, for EN-DC measurements. \n
			:param obw_limit: (float or boolean) numeric | ON | OFF Range: 10 MHz to 120 MHz, Unit: Hz ON | OFF enables or disables the limit check.
		"""
		param = Conversions.decimal_or_bool_value_to_str(obw_limit)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:SEMask:OBWLimit:ENDC {param}')

	def clone(self) -> 'ObwLimitCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ObwLimitCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
