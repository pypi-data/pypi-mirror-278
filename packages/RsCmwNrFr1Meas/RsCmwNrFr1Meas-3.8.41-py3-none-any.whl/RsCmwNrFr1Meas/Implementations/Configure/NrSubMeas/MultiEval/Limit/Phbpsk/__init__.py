from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhbpskCls:
	"""Phbpsk commands group definition. 8 total commands, 5 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phbpsk", core, parent)

	@property
	def evMagnitude(self):
		"""evMagnitude commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_evMagnitude'):
			from .EvMagnitude import EvMagnitudeCls
			self._evMagnitude = EvMagnitudeCls(self._core, self._cmd_group)
		return self._evMagnitude

	@property
	def merror(self):
		"""merror commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_merror'):
			from .Merror import MerrorCls
			self._merror = MerrorCls(self._core, self._cmd_group)
		return self._merror

	@property
	def perror(self):
		"""perror commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_perror'):
			from .Perror import PerrorCls
			self._perror = PerrorCls(self._core, self._cmd_group)
		return self._perror

	@property
	def iqOffset(self):
		"""iqOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqOffset'):
			from .IqOffset import IqOffsetCls
			self._iqOffset = IqOffsetCls(self._core, self._cmd_group)
		return self._iqOffset

	@property
	def ibe(self):
		"""ibe commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ibe'):
			from .Ibe import IbeCls
			self._ibe = IbeCls(self._core, self._cmd_group)
		return self._ibe

	def get_freq_error(self) -> float or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:FERRor \n
		Snippet: value: float or bool = driver.configure.nrSubMeas.multiEval.limit.phbpsk.get_freq_error() \n
		Defines an upper limit for the carrier frequency error (Pi/2-BPSK modulation) . \n
			:return: frequency_error: (float or boolean) numeric | ON | OFF Range: 0 ppm to 1 ppm, Unit: ppm ON | OFF enables or disables the limit check.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:FERRor?')
		return Conversions.str_to_float_or_bool(response)

	def set_freq_error(self, frequency_error: float or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:FERRor \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.phbpsk.set_freq_error(frequency_error = 1.0) \n
		Defines an upper limit for the carrier frequency error (Pi/2-BPSK modulation) . \n
			:param frequency_error: (float or boolean) numeric | ON | OFF Range: 0 ppm to 1 ppm, Unit: ppm ON | OFF enables or disables the limit check.
		"""
		param = Conversions.decimal_or_bool_value_to_str(frequency_error)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:FERRor {param}')

	# noinspection PyTypeChecker
	class EsFlatnessStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Fields: \n
			- Enable: bool: OFF | ON OFF: disables the limit check ON: enables the limit check
			- Range_1: float: numeric Upper limit for max(range 1) - min(range 1) Range: -256 dBpp to 256 dBpp, Unit: dBpp
			- Range_2: float: numeric Upper limit for max(range 2) - min(range 2) Range: -256 dBpp to 256 dBpp, Unit: dBpp
			- Max_1_Min_2: float: numeric Upper limit for max(range 1) - min(range 2) Range: -256 dB to 256 dB, Unit: dB
			- Max_2_Min_1: float: numeric Upper limit for max(range 2) - min(range 1) Range: -256 dB to 256 dB, Unit: dB
			- Edge_Frequency: float: numeric Band edge distance of border between range 1 and range 2 Range: 0 MHz to 20 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Range_1'),
			ArgStruct.scalar_float('Range_2'),
			ArgStruct.scalar_float('Max_1_Min_2'),
			ArgStruct.scalar_float('Max_2_Min_1'),
			ArgStruct.scalar_float('Edge_Frequency')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Range_1: float = None
			self.Range_2: float = None
			self.Max_1_Min_2: float = None
			self.Max_2_Min_1: float = None
			self.Edge_Frequency: float = None

	def get_es_flatness(self) -> EsFlatnessStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:ESFLatness \n
		Snippet: value: EsFlatnessStruct = driver.configure.nrSubMeas.multiEval.limit.phbpsk.get_es_flatness() \n
		Defines limits for the equalizer spectrum flatness (Pi/2-BPSK modulation) . \n
			:return: structure: for return value, see the help for EsFlatnessStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:ESFLatness?', self.__class__.EsFlatnessStruct())

	def set_es_flatness(self, value: EsFlatnessStruct) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:ESFLatness \n
		Snippet with structure: \n
		structure = driver.configure.nrSubMeas.multiEval.limit.phbpsk.EsFlatnessStruct() \n
		structure.Enable: bool = False \n
		structure.Range_1: float = 1.0 \n
		structure.Range_2: float = 1.0 \n
		structure.Max_1_Min_2: float = 1.0 \n
		structure.Max_2_Min_1: float = 1.0 \n
		structure.Edge_Frequency: float = 1.0 \n
		driver.configure.nrSubMeas.multiEval.limit.phbpsk.set_es_flatness(value = structure) \n
		Defines limits for the equalizer spectrum flatness (Pi/2-BPSK modulation) . \n
			:param value: see the help for EsFlatnessStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:PHBPsk:ESFLatness', value)

	def clone(self) -> 'PhbpskCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PhbpskCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
