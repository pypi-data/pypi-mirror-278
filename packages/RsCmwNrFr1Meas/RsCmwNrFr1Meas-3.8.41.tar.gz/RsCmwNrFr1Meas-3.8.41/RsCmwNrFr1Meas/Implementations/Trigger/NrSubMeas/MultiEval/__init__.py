from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiEvalCls:
	"""MultiEval commands group definition. 9 total commands, 1 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("multiEval", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import CatalogCls
			self._catalog = CatalogCls(self._core, self._cmd_group)
		return self._catalog

	def get_source(self) -> str:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:SOURce \n
		Snippet: value: str = driver.trigger.nrSubMeas.multiEval.get_source() \n
		Selects the source of the trigger events. Some values are always available. They are listed below. Depending on the
		installed options, additional values are available. You can query a list of all supported values via TRIGger:...
		:CATalog:SOURce?. \n
			:return: source: string 'Free Run (Fast Sync) ' Free run with synchronization 'Free Run (No Sync) ' Free run without synchronization 'IF Power' Power trigger (received RF power)
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:MEValuation:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:SOURce \n
		Snippet: driver.trigger.nrSubMeas.multiEval.set_source(source = 'abc') \n
		Selects the source of the trigger events. Some values are always available. They are listed below. Depending on the
		installed options, additional values are available. You can query a list of all supported values via TRIGger:...
		:CATalog:SOURce?. \n
			:param source: string 'Free Run (Fast Sync) ' Free run with synchronization 'Free Run (No Sync) ' Free run without synchronization 'IF Power' Power trigger (received RF power)
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:MEValuation:SOURce {param}')

	def get_threshold(self) -> float or bool:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:THReshold \n
		Snippet: value: float or bool = driver.trigger.nrSubMeas.multiEval.get_threshold() \n
		Defines the trigger threshold for power trigger sources. \n
			:return: trig_threshold: (float or boolean) numeric Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to reference level minus external attenuation)
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:MEValuation:THReshold?')
		return Conversions.str_to_float_or_bool(response)

	def set_threshold(self, trig_threshold: float or bool) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:THReshold \n
		Snippet: driver.trigger.nrSubMeas.multiEval.set_threshold(trig_threshold = 1.0) \n
		Defines the trigger threshold for power trigger sources. \n
			:param trig_threshold: (float or boolean) numeric Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to reference level minus external attenuation)
		"""
		param = Conversions.decimal_or_bool_value_to_str(trig_threshold)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:MEValuation:THReshold {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlope:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:SLOPe \n
		Snippet: value: enums.SignalSlope = driver.trigger.nrSubMeas.multiEval.get_slope() \n
		Qualifies whether the trigger event is generated at the rising or at the falling edge of the trigger pulse (valid for
		external and power trigger sources) . \n
			:return: slope: REDGe | FEDGe REDGe: Rising edge FEDGe: Falling edge
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:MEValuation:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlope)

	def set_slope(self, slope: enums.SignalSlope) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:SLOPe \n
		Snippet: driver.trigger.nrSubMeas.multiEval.set_slope(slope = enums.SignalSlope.FEDGe) \n
		Qualifies whether the trigger event is generated at the rising or at the falling edge of the trigger pulse (valid for
		external and power trigger sources) . \n
			:param slope: REDGe | FEDGe REDGe: Rising edge FEDGe: Falling edge
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SignalSlope)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:MEValuation:SLOPe {param}')

	def get_delay(self) -> float:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:DELay \n
		Snippet: value: float = driver.trigger.nrSubMeas.multiEval.get_delay() \n
		Defines a time delaying the start of the measurement relative to the trigger event. This setting has no influence on free
		run measurements. \n
			:return: delay: numeric Unit: s
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:MEValuation:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:DELay \n
		Snippet: driver.trigger.nrSubMeas.multiEval.set_delay(delay = 1.0) \n
		Defines a time delaying the start of the measurement relative to the trigger event. This setting has no influence on free
		run measurements. \n
			:param delay: numeric Unit: s
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:MEValuation:DELay {param}')

	def get_timeout(self) -> float or bool:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: value: float or bool = driver.trigger.nrSubMeas.multiEval.get_timeout() \n
		Selects the maximum time that the measurement waits for a trigger event before it stops in remote control mode or
		indicates a trigger timeout in manual operation mode. This setting has no influence on 'Free Run' measurements. \n
			:return: trigger_timeout: (float or boolean) numeric | ON | OFF Range: 0.01 s to 167772.15 s, Unit: s ON | OFF enables or disables the timeout check.
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:MEValuation:TOUT?')
		return Conversions.str_to_float_or_bool(response)

	def set_timeout(self, trigger_timeout: float or bool) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: driver.trigger.nrSubMeas.multiEval.set_timeout(trigger_timeout = 1.0) \n
		Selects the maximum time that the measurement waits for a trigger event before it stops in remote control mode or
		indicates a trigger timeout in manual operation mode. This setting has no influence on 'Free Run' measurements. \n
			:param trigger_timeout: (float or boolean) numeric | ON | OFF Range: 0.01 s to 167772.15 s, Unit: s ON | OFF enables or disables the timeout check.
		"""
		param = Conversions.decimal_or_bool_value_to_str(trigger_timeout)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:MEValuation:TOUT {param}')

	def get_mgap(self) -> float:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:MGAP \n
		Snippet: value: float = driver.trigger.nrSubMeas.multiEval.get_mgap() \n
		Sets a minimum time during which the IF signal must be below the trigger threshold before the trigger is armed so that an
		IF power trigger event can be generated. \n
			:return: min_trig_gap: numeric Range: 0 s to 1E-3 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:MEValuation:MGAP?')
		return Conversions.str_to_float(response)

	def set_mgap(self, min_trig_gap: float) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:MGAP \n
		Snippet: driver.trigger.nrSubMeas.multiEval.set_mgap(min_trig_gap = 1.0) \n
		Sets a minimum time during which the IF signal must be below the trigger threshold before the trigger is armed so that an
		IF power trigger event can be generated. \n
			:param min_trig_gap: numeric Range: 0 s to 1E-3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(min_trig_gap)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:MEValuation:MGAP {param}')

	# noinspection PyTypeChecker
	def get_smode(self) -> enums.SyncMode:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:SMODe \n
		Snippet: value: enums.SyncMode = driver.trigger.nrSubMeas.multiEval.get_smode() \n
		Selects the size of the search window for synchronization. \n
			:return: sync_mode: NORMal | ENHanced | NSSLot | ESSLot Normal, enhanced, normal single slot, enhanced single slot
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:MEValuation:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.SyncMode)

	def set_smode(self, sync_mode: enums.SyncMode) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:SMODe \n
		Snippet: driver.trigger.nrSubMeas.multiEval.set_smode(sync_mode = enums.SyncMode.ENHanced) \n
		Selects the size of the search window for synchronization. \n
			:param sync_mode: NORMal | ENHanced | NSSLot | ESSLot Normal, enhanced, normal single slot, enhanced single slot
		"""
		param = Conversions.enum_scalar_to_str(sync_mode, enums.SyncMode)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:MEValuation:SMODe {param}')

	def get_fsync(self) -> bool:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:FSYNc \n
		Snippet: value: bool = driver.trigger.nrSubMeas.multiEval.get_fsync() \n
		Enables frame synchronization for 'Free Run (Fast Sync) ' and 'IF Power'. \n
			:return: frame_sync: OFF | ON OFF: slot synchronization ON: frame synchronization
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:MEValuation:FSYNc?')
		return Conversions.str_to_bool(response)

	def set_fsync(self, frame_sync: bool) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:MEValuation:FSYNc \n
		Snippet: driver.trigger.nrSubMeas.multiEval.set_fsync(frame_sync = False) \n
		Enables frame synchronization for 'Free Run (Fast Sync) ' and 'IF Power'. \n
			:param frame_sync: OFF | ON OFF: slot synchronization ON: frame synchronization
		"""
		param = Conversions.bool_to_str(frame_sync)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:MEValuation:FSYNc {param}')

	def clone(self) -> 'MultiEvalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiEvalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
