from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeMaskCls:
	"""SeMask commands group definition. 14 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("seMask", core, parent)

	@property
	def rbw(self):
		"""rbw commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_rbw'):
			from .Rbw import RbwCls
			self._rbw = RbwCls(self._core, self._cmd_group)
		return self._rbw

	@property
	def area(self):
		"""area commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_area'):
			from .Area import AreaCls
			self._area = AreaCls(self._core, self._cmd_group)
		return self._area

	def clone(self) -> 'SeMaskCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SeMaskCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
