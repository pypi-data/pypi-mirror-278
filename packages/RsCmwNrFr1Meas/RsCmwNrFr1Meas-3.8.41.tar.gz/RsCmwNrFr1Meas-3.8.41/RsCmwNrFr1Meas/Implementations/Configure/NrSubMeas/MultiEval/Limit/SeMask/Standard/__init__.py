from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardCls:
	"""Standard commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("standard", core, parent)

	@property
	def obwLimit(self):
		"""obwLimit commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_obwLimit'):
			from .ObwLimit import ObwLimitCls
			self._obwLimit = ObwLimitCls(self._core, self._cmd_group)
		return self._obwLimit

	@property
	def area(self):
		"""area commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_area'):
			from .Area import AreaCls
			self._area = AreaCls(self._core, self._cmd_group)
		return self._area

	def clone(self) -> 'StandardCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StandardCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
