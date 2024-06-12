from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SetupCls:
	"""Setup commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setup", core, parent)

	# noinspection PyTypeChecker
	class SetupStruct(StructBase):
		"""Structure for setting input parameters. Contains optional setting parameters. Fields: \n
			- Segment_Length: int: No parameter help available
			- Level: float: No parameter help available
			- Duplex_Mode: enums.DuplexModeB: No parameter help available
			- Band: enums.Band: No parameter help available
			- Frequency: float: No parameter help available
			- Sub_Carr_Spacing: enums.SubCarrSpacing: No parameter help available
			- Ch_Bandwidth: enums.ChannelBwidth: No parameter help available
			- Cyclic_Prefix: enums.CyclicPrefix: No parameter help available
			- Channel_Type: enums.ChannelTypeA: No parameter help available
			- Dft_Precoding: bool: No parameter help available
			- Retrigger_Flag: enums.RetriggerFlag: No parameter help available
			- Evaluat_Offset: int: No parameter help available
			- Network_Sig_Val: enums.NetworkSigVal: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Segment_Length'),
			ArgStruct.scalar_float('Level'),
			ArgStruct.scalar_enum('Duplex_Mode', enums.DuplexModeB),
			ArgStruct.scalar_enum('Band', enums.Band),
			ArgStruct.scalar_float('Frequency'),
			ArgStruct.scalar_enum('Sub_Carr_Spacing', enums.SubCarrSpacing),
			ArgStruct.scalar_enum('Ch_Bandwidth', enums.ChannelBwidth),
			ArgStruct.scalar_enum('Cyclic_Prefix', enums.CyclicPrefix),
			ArgStruct.scalar_enum('Channel_Type', enums.ChannelTypeA),
			ArgStruct.scalar_bool('Dft_Precoding'),
			ArgStruct.scalar_enum('Retrigger_Flag', enums.RetriggerFlag),
			ArgStruct.scalar_int('Evaluat_Offset'),
			ArgStruct.scalar_enum_optional('Network_Sig_Val', enums.NetworkSigVal)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Segment_Length: int = None
			self.Level: float = None
			self.Duplex_Mode: enums.DuplexModeB = None
			self.Band: enums.Band = None
			self.Frequency: float = None
			self.Sub_Carr_Spacing: enums.SubCarrSpacing = None
			self.Ch_Bandwidth: enums.ChannelBwidth = None
			self.Cyclic_Prefix: enums.CyclicPrefix = None
			self.Channel_Type: enums.ChannelTypeA = None
			self.Dft_Precoding: bool = None
			self.Retrigger_Flag: enums.RetriggerFlag = None
			self.Evaluat_Offset: int = None
			self.Network_Sig_Val: enums.NetworkSigVal = None

	def set(self, structure: SetupStruct, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:SETup \n
		Snippet with structure: \n
		structure = driver.configure.nrSubMeas.multiEval.listPy.segment.setup.SetupStruct() \n
		structure.Segment_Length: int = 1 \n
		structure.Level: float = 1.0 \n
		structure.Duplex_Mode: enums.DuplexModeB = enums.DuplexModeB.FDD \n
		structure.Band: enums.Band = enums.Band.OB1 \n
		structure.Frequency: float = 1.0 \n
		structure.Sub_Carr_Spacing: enums.SubCarrSpacing = enums.SubCarrSpacing.S15K \n
		structure.Ch_Bandwidth: enums.ChannelBwidth = enums.ChannelBwidth.B005 \n
		structure.Cyclic_Prefix: enums.CyclicPrefix = enums.CyclicPrefix.EXTended \n
		structure.Channel_Type: enums.ChannelTypeA = enums.ChannelTypeA.PUCCh \n
		structure.Dft_Precoding: bool = False \n
		structure.Retrigger_Flag: enums.RetriggerFlag = enums.RetriggerFlag.IFPNarrowband \n
		structure.Evaluat_Offset: int = 1 \n
		structure.Network_Sig_Val: enums.NetworkSigVal = enums.NetworkSigVal.NS01 \n
		driver.configure.nrSubMeas.multiEval.listPy.segment.setup.set(structure, sEGMent = repcap.SEGMent.Default) \n
		No command help available \n
			:param structure: for set value, see the help for SetupStruct structure arguments.
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:SETup', structure)

	def get(self, sEGMent=repcap.SEGMent.Default) -> SetupStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:SETup \n
		Snippet: value: SetupStruct = driver.configure.nrSubMeas.multiEval.listPy.segment.setup.get(sEGMent = repcap.SEGMent.Default) \n
		No command help available \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for SetupStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:SETup?', self.__class__.SetupStruct())
