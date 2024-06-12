from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TtoleranceCls:
	"""Ttolerance commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ttolerance", core, parent)

	@property
	def cblt(self):
		"""cblt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cblt'):
			from .Cblt import CbltCls
			self._cblt = CbltCls(self._core, self._cmd_group)
		return self._cblt

	@property
	def cbgt(self):
		"""cbgt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbgt'):
			from .Cbgt import CbgtCls
			self._cbgt = CbgtCls(self._core, self._cmd_group)
		return self._cbgt

	def clone(self) -> 'TtoleranceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TtoleranceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
