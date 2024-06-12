from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SetupCls:
	"""Setup commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setup", core, parent)

	# noinspection PyTypeChecker
	class SetupStruct(StructBase):
		"""Structure for setting input parameters. Contains optional setting parameters. Fields: \n
			- Segment_Length: int: integer Number of subframes in the segment Range: 1 to 1000
			- Level: float: numeric Expected nominal power in the segment. The range can be calculated as follows: Range (Expected Nominal Power) = Range (Input Power) + External Attenuation - User Margin The input power range is stated in the specifications document. Unit: dBm
			- Duplex_Mode: enums.DuplexModeB: FDD | TDD Duplex mode used in the segment
			- Band: enums.Band: FDD: OB1 | OB2 | OB3 | OB5 | OB7 | OB8 | OB12 | OB13 | OB14 | OB18 | OB20 | OB24 | OB25 | OB26 | OB28 | OB30 | OB65 | OB66 | OB70 | OB71 | OB74 | OB80 | ... | OB86 | OB89 | OB91 | ... | OB95 | OB97 | OB98 | OB99 | OB105 | OB255 | OB256 TDD: OB34 | OB38 | ... | OB41 | OB46 | OB47 | OB48 | OB50 | OB51 | OB53 | OB77 | ... | OB84 | OB86 | OB89 | OB90 | OB95 | OB97 | OB98 | OB99 Operating band used in the segment
			- Retrigger_Flag: enums.RetriggerFlag: OFF | ON | IFPower | IFPNarrowband Specifies whether the measurement waits for a trigger event before measuring the segment, or not. The retrigger flag is ignored for trigger mode ONCE and evaluated for trigger mode SEGMent, see [CMDLINKRESOLVED Trigger.NrSubMeas.ListPy#Mode CMDLINKRESOLVED]. OFF Measure the segment without retrigger. For the first segment, the value OFF is interpreted as ON. ON Wait for a trigger event from the trigger source configured via [CMDLINKRESOLVED Trigger.NrSubMeas.MultiEval#Source CMDLINKRESOLVED]. IFPower Wait for a trigger event from the trigger source 'IF Power'. The trigger evaluation bandwidth is 160 MHz. IFPNarrowband Wait for a trigger event from the trigger source 'IF Power'. The trigger evaluation bandwidth is configured via [CMDLINKRESOLVED Trigger.NrSubMeas.ListPy#Nbandwidth CMDLINKRESOLVED].
			- Evaluat_Offset: int: integer Number of subframes at the beginning of the segment that are not evaluated Range: 0 to 1000
			- Network_Sig_Val: enums.NetworkSigVal: Optional setting parameter. NS01 | NS02 | NS03 | NS04 | NS05 | NS06 | NS07 | NS08 | NS09 | NS10 | NS11 | NS12 | NS13 | NS14 | NS15 | NS16 | NS17 | NS18 | NS19 | NS20 | NS21 | NS22 | NS23 | NS24 | NS25 | NS26 | NS27 | NS28 | NS29 | NS30 | NS31 | NS32 | NS35 Network signaled value to be used for the segment"""
		__meta_args_list = [
			ArgStruct.scalar_int('Segment_Length'),
			ArgStruct.scalar_float('Level'),
			ArgStruct.scalar_enum('Duplex_Mode', enums.DuplexModeB),
			ArgStruct.scalar_enum('Band', enums.Band),
			ArgStruct.scalar_enum('Retrigger_Flag', enums.RetriggerFlag),
			ArgStruct.scalar_int('Evaluat_Offset'),
			ArgStruct.scalar_enum_optional('Network_Sig_Val', enums.NetworkSigVal)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Segment_Length: int = None
			self.Level: float = None
			self.Duplex_Mode: enums.DuplexModeB = None
			self.Band: enums.Band = None
			self.Retrigger_Flag: enums.RetriggerFlag = None
			self.Evaluat_Offset: int = None
			self.Network_Sig_Val: enums.NetworkSigVal = None

	def set(self, structure: SetupStruct, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>:SETup \n
		Snippet with structure: \n
		structure = driver.configure.nrSubMeas.listPy.segment.setup.SetupStruct() \n
		structure.Segment_Length: int = 1 \n
		structure.Level: float = 1.0 \n
		structure.Duplex_Mode: enums.DuplexModeB = enums.DuplexModeB.FDD \n
		structure.Band: enums.Band = enums.Band.OB1 \n
		structure.Retrigger_Flag: enums.RetriggerFlag = enums.RetriggerFlag.IFPNarrowband \n
		structure.Evaluat_Offset: int = 1 \n
		structure.Network_Sig_Val: enums.NetworkSigVal = enums.NetworkSigVal.NS01 \n
		driver.configure.nrSubMeas.listPy.segment.setup.set(structure, sEGMent = repcap.SEGMent.Default) \n
		Defines the length and analyzer settings of segment <no>. For carrier-specific settings, there are additional commands.
		This command and the other segment configuration commands must be sent for all segments to be measured (method
		RsCmwNrFr1Meas.Configure.NrSubMeas.MultiEval.ListPy.Lrange.set) . \n
			:param structure: for set value, see the help for SetupStruct structure arguments.
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write_struct(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:SETup', structure)

	def get(self, sEGMent=repcap.SEGMent.Default) -> SetupStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>:SETup \n
		Snippet: value: SetupStruct = driver.configure.nrSubMeas.listPy.segment.setup.get(sEGMent = repcap.SEGMent.Default) \n
		Defines the length and analyzer settings of segment <no>. For carrier-specific settings, there are additional commands.
		This command and the other segment configuration commands must be sent for all segments to be measured (method
		RsCmwNrFr1Meas.Configure.NrSubMeas.MultiEval.ListPy.Lrange.set) . \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: structure: for return value, see the help for SetupStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:SETup?', self.__class__.SetupStruct())
