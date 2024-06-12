from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AreaCls:
	"""Area commands group definition. 2 total commands, 2 Subgroups, 0 group commands
	Repeated Capability: AreaReduced, default value after init: AreaReduced.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("area", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_areaReduced_get', 'repcap_areaReduced_set', repcap.AreaReduced.Nr1)

	def repcap_areaReduced_set(self, areaReduced: repcap.AreaReduced) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AreaReduced.Default
		Default value after init: AreaReduced.Nr1"""
		self._cmd_group.set_repcap_enum_value(areaReduced)

	def repcap_areaReduced_get(self) -> repcap.AreaReduced:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def endc(self):
		"""endc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_endc'):
			from .Endc import EndcCls
			self._endc = EndcCls(self._core, self._cmd_group)
		return self._endc

	@property
	def caggregation(self):
		"""caggregation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_caggregation'):
			from .Caggregation import CaggregationCls
			self._caggregation = CaggregationCls(self._core, self._cmd_group)
		return self._caggregation

	def clone(self) -> 'AreaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AreaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
