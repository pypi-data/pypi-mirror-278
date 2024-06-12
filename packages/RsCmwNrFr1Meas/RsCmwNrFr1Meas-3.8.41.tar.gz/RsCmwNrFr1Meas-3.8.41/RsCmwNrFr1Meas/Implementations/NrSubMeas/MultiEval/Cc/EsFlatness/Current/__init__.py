from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	@property
	def scIndex(self):
		"""scIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scIndex'):
			from .ScIndex import ScIndexCls
			self._scIndex = ScIndexCls(self._core, self._cmd_group)
		return self._scIndex

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tolerance: int: decimal Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits. Unit: %
			- Ripple_1: float: float Max (range 1) - min (range 1) Unit: dB
			- Ripple_2: float: float Max (range 2) - min (range 2) Unit: dB
			- Max_R_1_Min_R_2: float: float Max (range 1) - min (range 2) Unit: dB
			- Max_R_2_Min_R_1: float: float Max (range 2) - min (range 1) Unit: dB
			- Min_R_1: float: float Min (range 1) Unit: dB
			- Max_R_1: float: float Max (range 1) Unit: dB
			- Min_R_2: float: float Min (range 2) Unit: dB
			- Max_R_2: float: float Max (range 2) Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Ripple_1'),
			ArgStruct.scalar_float('Ripple_2'),
			ArgStruct.scalar_float('Max_R_1_Min_R_2'),
			ArgStruct.scalar_float('Max_R_2_Min_R_1'),
			ArgStruct.scalar_float('Min_R_1'),
			ArgStruct.scalar_float('Max_R_1'),
			ArgStruct.scalar_float('Min_R_2'),
			ArgStruct.scalar_float('Max_R_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Ripple_1: float = None
			self.Ripple_2: float = None
			self.Max_R_1_Min_R_2: float = None
			self.Max_R_2_Min_R_1: float = None
			self.Min_R_1: float = None
			self.Max_R_1: float = None
			self.Min_R_2: float = None
			self.Max_R_2: float = None

	def read(self, carrierComponent=repcap.CarrierComponent.Default) -> ResultData:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation[:CC<no>]:ESFLatness:CURRent \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.esFlatness.current.read(carrierComponent = repcap.CarrierComponent.Default) \n
		Return current, average, extreme and standard deviation single-value results of the equalizer spectrum flatness
		measurement, for carrier <no>. See also 'Equalizer spectrum flatness limits'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'READ:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:ESFLatness:CURRent?', self.__class__.ResultData())

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> ResultData:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation[:CC<no>]:ESFLatness:CURRent \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.esFlatness.current.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return current, average, extreme and standard deviation single-value results of the equalizer spectrum flatness
		measurement, for carrier <no>. See also 'Equalizer spectrum flatness limits'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:ESFLatness:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tolerance: int: decimal Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits. Unit: %
			- Ripple_1: float or bool: Limit check result for max (range 1) - min (range 1) .
			- Ripple_2: float or bool: Limit check result for max (range 2) - min (range 2) .
			- Max_R_1_Min_R_2: float or bool: Limit check result for max (range 1) - min (range 2) .
			- Max_R_2_Min_R_1: float or bool: Limit check result for max (range 2) - min (range 1) ."""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float_ext('Ripple_1'),
			ArgStruct.scalar_float_ext('Ripple_2'),
			ArgStruct.scalar_float_ext('Max_R_1_Min_R_2'),
			ArgStruct.scalar_float_ext('Max_R_2_Min_R_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tolerance: int = None
			self.Ripple_1: float or bool = None
			self.Ripple_2: float or bool = None
			self.Max_R_1_Min_R_2: float or bool = None
			self.Max_R_2_Min_R_1: float or bool = None

	def calculate(self, carrierComponent=repcap.CarrierComponent.Default) -> CalculateStruct:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation[:CC<no>]:ESFLatness:CURRent \n
		Snippet: value: CalculateStruct = driver.nrSubMeas.multiEval.cc.esFlatness.current.calculate(carrierComponent = repcap.CarrierComponent.Default) \n
		Return current, average and extreme limit check results for the equalizer spectrum flatness measurement, for carrier <no>.
		See also 'Equalizer spectrum flatness limits'. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:ESFLatness:CURRent?', self.__class__.CalculateStruct())

	def clone(self) -> 'CurrentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CurrentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
