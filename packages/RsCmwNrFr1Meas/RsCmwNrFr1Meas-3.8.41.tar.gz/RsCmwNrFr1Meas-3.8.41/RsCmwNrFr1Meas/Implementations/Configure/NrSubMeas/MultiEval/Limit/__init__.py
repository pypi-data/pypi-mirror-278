from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LimitCls:
	"""Limit commands group definition. 55 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("limit", core, parent)

	@property
	def phbpsk(self):
		"""phbpsk commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_phbpsk'):
			from .Phbpsk import PhbpskCls
			self._phbpsk = PhbpskCls(self._core, self._cmd_group)
		return self._phbpsk

	@property
	def bpwShaping(self):
		"""bpwShaping commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpwShaping'):
			from .BpwShaping import BpwShapingCls
			self._bpwShaping = BpwShapingCls(self._core, self._cmd_group)
		return self._bpwShaping

	@property
	def qpsk(self):
		"""qpsk commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_qpsk'):
			from .Qpsk import QpskCls
			self._qpsk = QpskCls(self._core, self._cmd_group)
		return self._qpsk

	@property
	def qam(self):
		"""qam commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_qam'):
			from .Qam import QamCls
			self._qam = QamCls(self._core, self._cmd_group)
		return self._qam

	@property
	def seMask(self):
		"""seMask commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_seMask'):
			from .SeMask import SeMaskCls
			self._seMask = SeMaskCls(self._core, self._cmd_group)
		return self._seMask

	@property
	def aclr(self):
		"""aclr commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_aclr'):
			from .Aclr import AclrCls
			self._aclr = AclrCls(self._core, self._cmd_group)
		return self._aclr

	@property
	def pdynamics(self):
		"""pdynamics commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_pdynamics'):
			from .Pdynamics import PdynamicsCls
			self._pdynamics = PdynamicsCls(self._core, self._cmd_group)
		return self._pdynamics

	def clone(self) -> 'LimitCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LimitCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
