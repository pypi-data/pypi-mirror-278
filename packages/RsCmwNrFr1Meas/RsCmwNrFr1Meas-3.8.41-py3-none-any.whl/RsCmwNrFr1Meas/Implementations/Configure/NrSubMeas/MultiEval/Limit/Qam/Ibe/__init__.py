from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


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
	class IbeStruct(StructBase):
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

	def set(self, structure: IbeStruct, qam=repcap.Qam.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM<order>:IBE \n
		Snippet with structure: \n
		structure = driver.configure.nrSubMeas.multiEval.limit.qam.ibe.IbeStruct() \n
		structure.Enable: bool = False \n
		structure.Minimum: float = 1.0 \n
		structure.Evm: float = 1.0 \n
		structure.Rb_Power: float = 1.0 \n
		structure.Iq_Image_Lesser: float = 1.0 \n
		structure.Iq_Image_Greater: float = 1.0 \n
		driver.configure.nrSubMeas.multiEval.limit.qam.ibe.set(structure, qam = repcap.Qam.Default) \n
		Defines parameters used for calculation of an upper limit for the inband emission (QAM modulations) , see 'Inband
		emissions limits'. \n
			:param structure: for set value, see the help for IbeStruct structure arguments.
			:param qam: optional repeated capability selector. Default value: Order16 (settable in the interface 'Qam')
		"""
		qam_cmd_val = self._cmd_group.get_repcap_cmd_value(qam, repcap.Qam)
		self._core.io.write_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM{qam_cmd_val}:IBE', structure)

	def get(self, qam=repcap.Qam.Default) -> IbeStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM<order>:IBE \n
		Snippet: value: IbeStruct = driver.configure.nrSubMeas.multiEval.limit.qam.ibe.get(qam = repcap.Qam.Default) \n
		Defines parameters used for calculation of an upper limit for the inband emission (QAM modulations) , see 'Inband
		emissions limits'. \n
			:param qam: optional repeated capability selector. Default value: Order16 (settable in the interface 'Qam')
			:return: structure: for return value, see the help for IbeStruct structure arguments."""
		qam_cmd_val = self._cmd_group.get_repcap_cmd_value(qam, repcap.Qam)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM{qam_cmd_val}:IBE?', self.__class__.IbeStruct())

	def clone(self) -> 'IbeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IbeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
