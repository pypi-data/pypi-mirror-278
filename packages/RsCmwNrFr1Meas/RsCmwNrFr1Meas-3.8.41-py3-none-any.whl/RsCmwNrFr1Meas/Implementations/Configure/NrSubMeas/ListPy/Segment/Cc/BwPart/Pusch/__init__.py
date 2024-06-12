from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PuschCls:
	"""Pusch commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pusch", core, parent)

	@property
	def dmta(self):
		"""dmta commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmta'):
			from .Dmta import DmtaCls
			self._dmta = DmtaCls(self._core, self._cmd_group)
		return self._dmta

	@property
	def dmtb(self):
		"""dmtb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmtb'):
			from .Dmtb import DmtbCls
			self._dmtb = DmtbCls(self._core, self._cmd_group)
		return self._dmtb

	@property
	def dftPrecoding(self):
		"""dftPrecoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dftPrecoding'):
			from .DftPrecoding import DftPrecodingCls
			self._dftPrecoding = DftPrecodingCls(self._core, self._cmd_group)
		return self._dftPrecoding

	def clone(self) -> 'PuschCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PuschCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
