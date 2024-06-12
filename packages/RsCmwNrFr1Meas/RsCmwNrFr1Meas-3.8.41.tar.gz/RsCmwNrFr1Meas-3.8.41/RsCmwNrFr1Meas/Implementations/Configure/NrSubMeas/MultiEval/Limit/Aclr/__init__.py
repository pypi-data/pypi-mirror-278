from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AclrCls:
	"""Aclr commands group definition. 5 total commands, 4 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("aclr", core, parent)

	@property
	def utra(self):
		"""utra commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_utra'):
			from .Utra import UtraCls
			self._utra = UtraCls(self._core, self._cmd_group)
		return self._utra

	@property
	def nr(self):
		"""nr commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nr'):
			from .Nr import NrCls
			self._nr = NrCls(self._core, self._cmd_group)
		return self._nr

	@property
	def ttolerance(self):
		"""ttolerance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttolerance'):
			from .Ttolerance import TtoleranceCls
			self._ttolerance = TtoleranceCls(self._core, self._cmd_group)
		return self._ttolerance

	@property
	def caggregation(self):
		"""caggregation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_caggregation'):
			from .Caggregation import CaggregationCls
			self._caggregation = CaggregationCls(self._core, self._cmd_group)
		return self._caggregation

	def get_endc(self) -> float or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:ACLR:ENDC \n
		Snippet: value: float or bool = driver.configure.nrSubMeas.multiEval.limit.aclr.get_endc() \n
		Defines a relative limit for the ACLR measured in an adjacent channel in EN-DC mode. \n
			:return: relative_level: (float or boolean) numeric | ON | OFF Relative lower ACLR limit without test tolerance Range: -256 dB to 256 dB, Unit: dB ON | OFF enables or disables the limit check.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:ACLR:ENDC?')
		return Conversions.str_to_float_or_bool(response)

	def set_endc(self, relative_level: float or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:ACLR:ENDC \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.aclr.set_endc(relative_level = 1.0) \n
		Defines a relative limit for the ACLR measured in an adjacent channel in EN-DC mode. \n
			:param relative_level: (float or boolean) numeric | ON | OFF Relative lower ACLR limit without test tolerance Range: -256 dB to 256 dB, Unit: dB ON | OFF enables or disables the limit check.
		"""
		param = Conversions.decimal_or_bool_value_to_str(relative_level)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:ACLR:ENDC {param}')

	def clone(self) -> 'AclrCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AclrCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
