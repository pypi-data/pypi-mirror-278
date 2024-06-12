from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CcCls:
	"""Cc commands group definition. 13 total commands, 8 Subgroups, 0 group commands
	Repeated Capability: CarrierComponent, default value after init: CarrierComponent.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cc", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_carrierComponent_get', 'repcap_carrierComponent_set', repcap.CarrierComponent.Nr1)

	def repcap_carrierComponent_set(self, carrierComponent: repcap.CarrierComponent) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CarrierComponent.Default
		Default value after init: CarrierComponent.Nr1"""
		self._cmd_group.set_repcap_enum_value(carrierComponent)

	def repcap_carrierComponent_get(self) -> repcap.CarrierComponent:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def txBwidth(self):
		"""txBwidth commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_txBwidth'):
			from .TxBwidth import TxBwidthCls
			self._txBwidth = TxBwidthCls(self._core, self._cmd_group)
		return self._txBwidth

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
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
	def plcId(self):
		"""plcId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plcId'):
			from .PlcId import PlcIdCls
			self._plcId = PlcIdCls(self._core, self._cmd_group)
		return self._plcId

	@property
	def taPosition(self):
		"""taPosition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_taPosition'):
			from .TaPosition import TaPositionCls
			self._taPosition = TaPositionCls(self._core, self._cmd_group)
		return self._taPosition

	@property
	def bwPart(self):
		"""bwPart commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_bwPart'):
			from .BwPart import BwPartCls
			self._bwPart = BwPartCls(self._core, self._cmd_group)
		return self._bwPart

	@property
	def nallocations(self):
		"""nallocations commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nallocations'):
			from .Nallocations import NallocationsCls
			self._nallocations = NallocationsCls(self._core, self._cmd_group)
		return self._nallocations

	@property
	def allocation(self):
		"""allocation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_allocation'):
			from .Allocation import AllocationCls
			self._allocation = AllocationCls(self._core, self._cmd_group)
		return self._allocation

	def clone(self) -> 'CcCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CcCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
