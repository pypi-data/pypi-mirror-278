from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CcallCls:
	"""Ccall commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ccall", core, parent)

	@property
	def txBwidth(self):
		"""txBwidth commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_txBwidth'):
			from .TxBwidth import TxBwidthCls
			self._txBwidth = TxBwidthCls(self._core, self._cmd_group)
		return self._txBwidth

	def clone(self) -> 'CcallCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CcallCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
