from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CaggregationCls:
	"""Caggregation commands group definition. 7 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("caggregation", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def cbandwidth(self):
		"""cbandwidth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbandwidth'):
			from .Cbandwidth import CbandwidthCls
			self._cbandwidth = CbandwidthCls(self._core, self._cmd_group)
		return self._cbandwidth

	@property
	def acSpacing(self):
		"""acSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acSpacing'):
			from .AcSpacing import AcSpacingCls
			self._acSpacing = AcSpacingCls(self._core, self._cmd_group)
		return self._acSpacing

	# noinspection PyTypeChecker
	def get_mcarrier(self) -> enums.CarrierComponent:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:CAGGregation:MCARrier \n
		Snippet: value: enums.CarrierComponent = driver.configure.nrSubMeas.caggregation.get_mcarrier() \n
		Selects a component carrier for synchronization and single-carrier measurements. \n
			:return: meas_carrier: CC1 | CC2
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:CAGGregation:MCARrier?')
		return Conversions.str_to_scalar_enum(response, enums.CarrierComponent)

	def set_mcarrier(self, meas_carrier: enums.CarrierComponent) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:CAGGregation:MCARrier \n
		Snippet: driver.configure.nrSubMeas.caggregation.set_mcarrier(meas_carrier = enums.CarrierComponent.CC1) \n
		Selects a component carrier for synchronization and single-carrier measurements. \n
			:param meas_carrier: CC1 | CC2
		"""
		param = Conversions.enum_scalar_to_str(meas_carrier, enums.CarrierComponent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CAGGregation:MCARrier {param}')

	# noinspection PyTypeChecker
	def get_dcarrier(self) -> enums.CarrierComponent:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:CAGGregation:DCARrier \n
		Snippet: value: enums.CarrierComponent = driver.configure.nrSubMeas.caggregation.get_dcarrier() \n
		No command help available \n
			:return: display_carrier: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:CAGGregation:DCARrier?')
		return Conversions.str_to_scalar_enum(response, enums.CarrierComponent)

	def set_dcarrier(self, display_carrier: enums.CarrierComponent) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:CAGGregation:DCARrier \n
		Snippet: driver.configure.nrSubMeas.caggregation.set_dcarrier(display_carrier = enums.CarrierComponent.CC1) \n
		No command help available \n
			:param display_carrier: No help available
		"""
		param = Conversions.enum_scalar_to_str(display_carrier, enums.CarrierComponent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:CAGGregation:DCARrier {param}')

	def clone(self) -> 'CaggregationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CaggregationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
