from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SegmentCls:
	"""Segment commands group definition. 68 total commands, 5 Subgroups, 0 group commands
	Repeated Capability: SEGMent, default value after init: SEGMent.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("segment", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_sEGMent_get', 'repcap_sEGMent_set', repcap.SEGMent.Nr1)

	def repcap_sEGMent_set(self, sEGMent: repcap.SEGMent) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SEGMent.Default
		Default value after init: SEGMent.Nr1"""
		self._cmd_group.set_repcap_enum_value(sEGMent)

	def repcap_sEGMent_get(self) -> repcap.SEGMent:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def cc(self):
		"""cc commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_cc'):
			from .Cc import CcCls
			self._cc = CcCls(self._core, self._cmd_group)
		return self._cc

	@property
	def seMask(self):
		"""seMask commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_seMask'):
			from .SeMask import SeMaskCls
			self._seMask = SeMaskCls(self._core, self._cmd_group)
		return self._seMask

	@property
	def aclr(self):
		"""aclr commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_aclr'):
			from .Aclr import AclrCls
			self._aclr = AclrCls(self._core, self._cmd_group)
		return self._aclr

	@property
	def power(self):
		"""power commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def pmonitor(self):
		"""pmonitor commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pmonitor'):
			from .Pmonitor import PmonitorCls
			self._pmonitor = PmonitorCls(self._core, self._cmd_group)
		return self._pmonitor

	def clone(self) -> 'SegmentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SegmentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
