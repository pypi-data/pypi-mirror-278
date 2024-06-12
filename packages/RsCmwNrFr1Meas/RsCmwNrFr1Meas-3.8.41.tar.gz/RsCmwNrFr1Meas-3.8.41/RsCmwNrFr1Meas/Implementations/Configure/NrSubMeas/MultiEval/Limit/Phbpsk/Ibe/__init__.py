from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IbeCls:
	"""Ibe commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ibe", core, parent)

	@property
	def iqOffset(self):
		"""iqOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqOffset'):
			from .IqOffset import IqOffsetCls
			self._iqOffset = IqOffsetCls(self._core, self._cmd_group)
		return self._iqOffset

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Fields: \n
			- Enable: bool: OFF | ON OFF: disables the limit check ON: enables the limit check
			- Minimum: float: numeric Range: -256 dB to 256 dB, Unit: dB
			- Evm: float: numeric Range: 0 % to 100 %, Unit: %
			- Rb_Power: float: numeric Range: -256 dBm to 256 dBm, Unit: dBm
			- Iq_Image_Lesser: float: numeric IQ image for low TX power range Range: -256 dB to 256 dB, Unit: dB
			- Iq_Image_Greater: float: numeric IQ image for high TX power range Range: -256 dB to 256 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Minimum'),
			ArgStruct.scalar_float('Evm'),
			ArgStruct.scalar_float('Rb_Power'),
			ArgStruct.scalar_float('Iq_Image_Lesser'),
			ArgStruct.scalar_float('Iq_Image_Greater')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Minimum: float = None
			self.Evm: float = None
			self.Rb_Power: float = None
			self.Iq_Image_Lesser: float = None
			self.Iq_Image_Greater: float = None

	def get_value(self) -> ValueStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:IBE \n
		Snippet: value: ValueStruct = driver.configure.nrSubMeas.multiEval.limit.phbpsk.ibe.get_value() \n
		Defines parameters used for calculation of an upper limit for the inband emission (Pi/2-BPSK modulation) , see 'Inband
		emissions limits'. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:IBE?', self.__class__.ValueStruct())

	def set_value(self, value: ValueStruct) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:IBE \n
		Snippet with structure: \n
		structure = driver.configure.nrSubMeas.multiEval.limit.phbpsk.ibe.ValueStruct() \n
		structure.Enable: bool = False \n
		structure.Minimum: float = 1.0 \n
		structure.Evm: float = 1.0 \n
		structure.Rb_Power: float = 1.0 \n
		structure.Iq_Image_Lesser: float = 1.0 \n
		structure.Iq_Image_Greater: float = 1.0 \n
		driver.configure.nrSubMeas.multiEval.limit.phbpsk.ibe.set_value(value = structure) \n
		Defines parameters used for calculation of an upper limit for the inband emission (Pi/2-BPSK modulation) , see 'Inband
		emissions limits'. \n
			:param value: see the help for ValueStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:IBE', value)

	def clone(self) -> 'IbeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IbeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
