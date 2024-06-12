from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeMaskCls:
	"""SeMask commands group definition. 14 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("seMask", core, parent)

	@property
	def obwLimit(self):
		"""obwLimit commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_obwLimit'):
			from .ObwLimit import ObwLimitCls
			self._obwLimit = ObwLimitCls(self._core, self._cmd_group)
		return self._obwLimit

	@property
	def area(self):
		"""area commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_area'):
			from .Area import AreaCls
			self._area = AreaCls(self._core, self._cmd_group)
		return self._area

	@property
	def ttolerance(self):
		"""ttolerance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttolerance'):
			from .Ttolerance import TtoleranceCls
			self._ttolerance = TtoleranceCls(self._core, self._cmd_group)
		return self._ttolerance

	@property
	def actLimit(self):
		"""actLimit commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_actLimit'):
			from .ActLimit import ActLimitCls
			self._actLimit = ActLimitCls(self._core, self._cmd_group)
		return self._actLimit

	@property
	def standard(self):
		"""standard commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_standard'):
			from .Standard import StandardCls
			self._standard = StandardCls(self._core, self._cmd_group)
		return self._standard

	@property
	def userDefined(self):
		"""userDefined commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_userDefined'):
			from .UserDefined import UserDefinedCls
			self._userDefined = UserDefinedCls(self._core, self._cmd_group)
		return self._userDefined

	def clone(self) -> 'SeMaskCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SeMaskCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
