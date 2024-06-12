from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiEvalCls:
	"""MultiEval commands group definition. 143 total commands, 15 Subgroups, 23 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("multiEval", core, parent)

	@property
	def bwConfig(self):
		"""bwConfig commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bwConfig'):
			from .BwConfig import BwConfigCls
			self._bwConfig = BwConfigCls(self._core, self._cmd_group)
		return self._bwConfig

	@property
	def pcomp(self):
		"""pcomp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcomp'):
			from .Pcomp import PcompCls
			self._pcomp = PcompCls(self._core, self._cmd_group)
		return self._pcomp

	@property
	def msubFrames(self):
		"""msubFrames commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_msubFrames'):
			from .MsubFrames import MsubFramesCls
			self._msubFrames = MsubFramesCls(self._core, self._cmd_group)
		return self._msubFrames

	@property
	def mslot(self):
		"""mslot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mslot'):
			from .Mslot import MslotCls
			self._mslot = MslotCls(self._core, self._cmd_group)
		return self._mslot

	@property
	def spectrum(self):
		"""spectrum commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_spectrum'):
			from .Spectrum import SpectrumCls
			self._spectrum = SpectrumCls(self._core, self._cmd_group)
		return self._spectrum

	@property
	def modulation(self):
		"""modulation commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Modulation import ModulationCls
			self._modulation = ModulationCls(self._core, self._cmd_group)
		return self._modulation

	@property
	def rbAllocation(self):
		"""rbAllocation commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_rbAllocation'):
			from .RbAllocation import RbAllocationCls
			self._rbAllocation = RbAllocationCls(self._core, self._cmd_group)
		return self._rbAllocation

	@property
	def allocation(self):
		"""allocation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_allocation'):
			from .Allocation import AllocationCls
			self._allocation = AllocationCls(self._core, self._cmd_group)
		return self._allocation

	@property
	def dmrs(self):
		"""dmrs commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_dmrs'):
			from .Dmrs import DmrsCls
			self._dmrs = DmrsCls(self._core, self._cmd_group)
		return self._dmrs

	@property
	def endc(self):
		"""endc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_endc'):
			from .Endc import EndcCls
			self._endc = EndcCls(self._core, self._cmd_group)
		return self._endc

	@property
	def pdynamics(self):
		"""pdynamics commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdynamics'):
			from .Pdynamics import PdynamicsCls
			self._pdynamics = PdynamicsCls(self._core, self._cmd_group)
		return self._pdynamics

	@property
	def scount(self):
		"""scount commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_scount'):
			from .Scount import ScountCls
			self._scount = ScountCls(self._core, self._cmd_group)
		return self._scount

	@property
	def result(self):
		"""result commands group. 1 Sub-classes, 13 commands."""
		if not hasattr(self, '_result'):
			from .Result import ResultCls
			self._result = ResultCls(self._core, self._cmd_group)
		return self._result

	@property
	def limit(self):
		"""limit commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	@property
	def listPy(self):
		"""listPy commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: value: float = driver.configure.nrSubMeas.multiEval.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually. When the measurement has completed the first measurement
		cycle (first single shot) , the statistical depth is reached and the timer is reset. If the first measurement cycle has
		not been completed when the timer expires, the measurement is stopped. The measurement state changes to RDY.
		The reliability indicator is set to 1, indicating that a measurement timeout occurred. Still running READ, FETCh or
		CALCulate commands are completed, returning the available results. At least for some results, there are no values at all
		or the statistical depth has not been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: timeout: numeric Unit: s
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, timeout: float) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_timeout(timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated manually. When the measurement has completed the first measurement
		cycle (first single shot) , the statistical depth is reached and the timer is reset. If the first measurement cycle has
		not been completed when the timer expires, the measurement is stopped. The measurement state changes to RDY.
		The reliability indicator is set to 1, indicating that a measurement timeout occurred. Still running READ, FETCh or
		CALCulate commands are completed, returning the available results. At least for some results, there are no values at all
		or the statistical depth has not been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param timeout: numeric Unit: s
		"""
		param = Conversions.decimal_value_to_str(timeout)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:TOUT {param}')

	# noinspection PyTypeChecker
	def get_dmode(self) -> enums.DuplexModeB:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMODe \n
		Snippet: value: enums.DuplexModeB = driver.configure.nrSubMeas.multiEval.get_dmode() \n
		Selects the duplex mode of the signal: FDD or TDD. \n
			:return: mode: FDD | TDD
		"""
		response = self._core.io.query_str_with_opc('CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMODe?')
		return Conversions.str_to_scalar_enum(response, enums.DuplexModeB)

	def set_dmode(self, mode: enums.DuplexModeB) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMODe \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_dmode(mode = enums.DuplexModeB.FDD) \n
		Selects the duplex mode of the signal: FDD or TDD. \n
			:param mode: FDD | TDD
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.DuplexModeB)
		self._core.io.write_with_opc(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:DMODe {param}')

	# noinspection PyTypeChecker
	def get_sc_spacing(self) -> enums.SubCarrSpacing:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCSPacing \n
		Snippet: value: enums.SubCarrSpacing = driver.configure.nrSubMeas.multiEval.get_sc_spacing() \n
		No command help available \n
			:return: sub_carr_spacing: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.SubCarrSpacing)

	def set_sc_spacing(self, sub_carr_spacing: enums.SubCarrSpacing) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCSPacing \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_sc_spacing(sub_carr_spacing = enums.SubCarrSpacing.S15K) \n
		No command help available \n
			:param sub_carr_spacing: No help available
		"""
		param = Conversions.enum_scalar_to_str(sub_carr_spacing, enums.SubCarrSpacing)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCSPacing {param}')

	# noinspection PyTypeChecker
	def get_cbandwidth(self) -> enums.ChannelBwidth:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:CBANdwidth \n
		Snippet: value: enums.ChannelBwidth = driver.configure.nrSubMeas.multiEval.get_cbandwidth() \n
		No command help available \n
			:return: channel_bw: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:CBANdwidth?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelBwidth)

	def set_cbandwidth(self, channel_bw: enums.ChannelBwidth) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:CBANdwidth \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_cbandwidth(channel_bw = enums.ChannelBwidth.B005) \n
		No command help available \n
			:param channel_bw: No help available
		"""
		param = Conversions.enum_scalar_to_str(channel_bw, enums.ChannelBwidth)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:CBANdwidth {param}')

	def get_dft_precoding(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DFTPrecoding \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.get_dft_precoding() \n
		No command help available \n
			:return: on_off: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:DFTPrecoding?')
		return Conversions.str_to_bool(response)

	def set_dft_precoding(self, on_off: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DFTPrecoding \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_dft_precoding(on_off = False) \n
		No command help available \n
			:param on_off: No help available
		"""
		param = Conversions.bool_to_str(on_off)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:DFTPrecoding {param}')

	# noinspection PyTypeChecker
	def get_mscheme(self) -> enums.ModulationScheme:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MSCHeme \n
		Snippet: value: enums.ModulationScheme = driver.configure.nrSubMeas.multiEval.get_mscheme() \n
		No command help available \n
			:return: mod_scheme: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:MSCHeme?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationScheme)

	def set_mscheme(self, mod_scheme: enums.ModulationScheme) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MSCHeme \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_mscheme(mod_scheme = enums.ModulationScheme.AUTO) \n
		No command help available \n
			:param mod_scheme: No help available
		"""
		param = Conversions.enum_scalar_to_str(mod_scheme, enums.ModulationScheme)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MSCHeme {param}')

	# noinspection PyTypeChecker
	def get_cprefix(self) -> enums.CyclicPrefix:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:CPRefix \n
		Snippet: value: enums.CyclicPrefix = driver.configure.nrSubMeas.multiEval.get_cprefix() \n
		No command help available \n
			:return: cyclic_prefix: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:CPRefix?')
		return Conversions.str_to_scalar_enum(response, enums.CyclicPrefix)

	def set_cprefix(self, cyclic_prefix: enums.CyclicPrefix) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:CPRefix \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_cprefix(cyclic_prefix = enums.CyclicPrefix.EXTended) \n
		No command help available \n
			:param cyclic_prefix: No help available
		"""
		param = Conversions.enum_scalar_to_str(cyclic_prefix, enums.CyclicPrefix)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:CPRefix {param}')

	# noinspection PyTypeChecker
	def get_ns_value(self) -> enums.NetworkSigVal:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:NSValue \n
		Snippet: value: enums.NetworkSigVal = driver.configure.nrSubMeas.multiEval.get_ns_value() \n
		Selects the 'network signaled value'. \n
			:return: value: NS01 | NS02 | NS03 | NS04 | NS05 | NS06 | NS07 | NS08 | NS09 | NS10 | NS11 | NS12 | NS13 | NS14 | NS15 | NS16 | NS17 | NS18 | NS19 | NS20 | NS21 | NS22 | NS23 | NS24 | NS25 | NS26 | NS27 | NS28 | NS29 | NS30 | NS31 | NS32 | NS35 Value NS_01 to NS_32, NS_35
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:NSValue?')
		return Conversions.str_to_scalar_enum(response, enums.NetworkSigVal)

	def set_ns_value(self, value: enums.NetworkSigVal) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:NSValue \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_ns_value(value = enums.NetworkSigVal.NS01) \n
		Selects the 'network signaled value'. \n
			:param value: NS01 | NS02 | NS03 | NS04 | NS05 | NS06 | NS07 | NS08 | NS09 | NS10 | NS11 | NS12 | NS13 | NS14 | NS15 | NS16 | NS17 | NS18 | NS19 | NS20 | NS21 | NS22 | NS23 | NS24 | NS25 | NS26 | NS27 | NS28 | NS29 | NS30 | NS31 | NS32 | NS35 Value NS_01 to NS_32, NS_35
		"""
		param = Conversions.enum_scalar_to_str(value, enums.NetworkSigVal)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:NSValue {param}')

	def get_plc_id(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PLCid \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.get_plc_id() \n
		No command help available \n
			:return: phs_layer_cell_id: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:PLCid?')
		return Conversions.str_to_int(response)

	def set_plc_id(self, phs_layer_cell_id: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PLCid \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_plc_id(phs_layer_cell_id = 1) \n
		No command help available \n
			:param phs_layer_cell_id: No help available
		"""
		param = Conversions.decimal_value_to_str(phs_layer_cell_id)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:PLCid {param}')

	# noinspection PyTypeChecker
	def get_ctype(self) -> enums.ChannelTypeA:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:CTYPe \n
		Snippet: value: enums.ChannelTypeA = driver.configure.nrSubMeas.multiEval.get_ctype() \n
		No command help available \n
			:return: channel_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:CTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelTypeA)

	def set_ctype(self, channel_type: enums.ChannelTypeA) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:CTYPe \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_ctype(channel_type = enums.ChannelTypeA.PUCCh) \n
		No command help available \n
			:param channel_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(channel_type, enums.ChannelTypeA)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:CTYPe {param}')

	# noinspection PyTypeChecker
	class PuschConfigStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Fields: \n
			- Mod_Scheme: enums.ModulationScheme: No parameter help available
			- Mapping_Type: enums.MappingType: No parameter help available
			- Nrb_Auto: bool: No parameter help available
			- No_Rb: int: No parameter help available
			- Start_Rb: int: No parameter help available
			- No_Symbols: int: No parameter help available
			- Start_Symbol: int: No parameter help available
			- Config_Type: enums.ConfigType: No parameter help available
			- Max_Length: enums.MaxLength: No parameter help available
			- Add_Position: int: No parameter help available
			- Lzero: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Mod_Scheme', enums.ModulationScheme),
			ArgStruct.scalar_enum('Mapping_Type', enums.MappingType),
			ArgStruct.scalar_bool('Nrb_Auto'),
			ArgStruct.scalar_int('No_Rb'),
			ArgStruct.scalar_int('Start_Rb'),
			ArgStruct.scalar_int('No_Symbols'),
			ArgStruct.scalar_int('Start_Symbol'),
			ArgStruct.scalar_enum('Config_Type', enums.ConfigType),
			ArgStruct.scalar_enum('Max_Length', enums.MaxLength),
			ArgStruct.scalar_int('Add_Position'),
			ArgStruct.scalar_int('Lzero')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mod_Scheme: enums.ModulationScheme = None
			self.Mapping_Type: enums.MappingType = None
			self.Nrb_Auto: bool = None
			self.No_Rb: int = None
			self.Start_Rb: int = None
			self.No_Symbols: int = None
			self.Start_Symbol: int = None
			self.Config_Type: enums.ConfigType = None
			self.Max_Length: enums.MaxLength = None
			self.Add_Position: int = None
			self.Lzero: int = None

	def get_pusch_config(self) -> PuschConfigStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PUSChconfig \n
		Snippet: value: PuschConfigStruct = driver.configure.nrSubMeas.multiEval.get_pusch_config() \n
		No command help available \n
			:return: structure: for return value, see the help for PuschConfigStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:NRSub:MEASurement<Instance>:MEValuation:PUSChconfig?', self.__class__.PuschConfigStruct())

	def set_pusch_config(self, value: PuschConfigStruct) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PUSChconfig \n
		Snippet with structure: \n
		structure = driver.configure.nrSubMeas.multiEval.PuschConfigStruct() \n
		structure.Mod_Scheme: enums.ModulationScheme = enums.ModulationScheme.AUTO \n
		structure.Mapping_Type: enums.MappingType = enums.MappingType.A \n
		structure.Nrb_Auto: bool = False \n
		structure.No_Rb: int = 1 \n
		structure.Start_Rb: int = 1 \n
		structure.No_Symbols: int = 1 \n
		structure.Start_Symbol: int = 1 \n
		structure.Config_Type: enums.ConfigType = enums.ConfigType.T1 \n
		structure.Max_Length: enums.MaxLength = enums.MaxLength.DOUBle \n
		structure.Add_Position: int = 1 \n
		structure.Lzero: int = 1 \n
		driver.configure.nrSubMeas.multiEval.set_pusch_config(value = structure) \n
		No command help available \n
			:param value: see the help for PuschConfigStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:NRSub:MEASurement<Instance>:MEValuation:PUSChconfig', value)

	# noinspection PyTypeChecker
	def get_map_type(self) -> enums.MappingType:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MAPType \n
		Snippet: value: enums.MappingType = driver.configure.nrSubMeas.multiEval.get_map_type() \n
		No command help available \n
			:return: mapping_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:MAPType?')
		return Conversions.str_to_scalar_enum(response, enums.MappingType)

	def set_map_type(self, mapping_type: enums.MappingType) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MAPType \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_map_type(mapping_type = enums.MappingType.A) \n
		No command help available \n
			:param mapping_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(mapping_type, enums.MappingType)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MAPType {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.nrSubMeas.multiEval.get_repetition() \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single shot or repeated continuously. Use CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
		intervals per single shot. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot: Single-shot measurement CONTinuous: Continuous measurement
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:REPetition \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single shot or repeated continuously. Use CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
		intervals per single shot. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot: Single-shot measurement CONTinuous: Continuous measurement
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:REPetition {param}')

	# noinspection PyTypeChecker
	def get_scondition(self) -> enums.StopCondition:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCONdition \n
		Snippet: value: enums.StopCondition = driver.configure.nrSubMeas.multiEval.get_scondition() \n
		Qualifies whether the measurement is stopped after a failed limit check or continued. SLFail means that the measurement
		is stopped and reaches the RDY state when one of the results exceeds the limits. \n
			:return: stop_condition: NONE | SLFail NONE: Continue measurement irrespective of the limit check. SLFail: Stop measurement on limit failure.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCONdition?')
		return Conversions.str_to_scalar_enum(response, enums.StopCondition)

	def set_scondition(self, stop_condition: enums.StopCondition) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCONdition \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_scondition(stop_condition = enums.StopCondition.NONE) \n
		Qualifies whether the measurement is stopped after a failed limit check or continued. SLFail means that the measurement
		is stopped and reaches the RDY state when one of the results exceeds the limits. \n
			:param stop_condition: NONE | SLFail NONE: Continue measurement irrespective of the limit check. SLFail: Stop measurement on limit failure.
		"""
		param = Conversions.enum_scalar_to_str(stop_condition, enums.StopCondition)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:SCONdition {param}')

	# noinspection PyTypeChecker
	def get_mmode(self) -> enums.MeasurementMode:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MMODe \n
		Snippet: value: enums.MeasurementMode = driver.configure.nrSubMeas.multiEval.get_mmode() \n
		Selects the measurement mode. \n
			:return: measurement_mode: NORMal | MELMode NORMal: normal mode MELMode: multi-evaluation list mode For a setting command, only NORMal is allowed (disables the list mode) . A query can also return MELM.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:MMODe?')
		return Conversions.str_to_scalar_enum(response, enums.MeasurementMode)

	def set_mmode(self, measurement_mode: enums.MeasurementMode) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MMODe \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_mmode(measurement_mode = enums.MeasurementMode.MELMode) \n
		Selects the measurement mode. \n
			:param measurement_mode: NORMal | MELMode NORMal: normal mode MELMode: multi-evaluation list mode For a setting command, only NORMal is allowed (disables the list mode) . A query can also return MELM.
		"""
		param = Conversions.enum_scalar_to_str(measurement_mode, enums.MeasurementMode)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MMODe {param}')

	def get_mo_exception(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MOEXception \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.get_mo_exception() \n
		Specifies whether measurement results identified as faulty or inaccurate are rejected. \n
			:return: meas_on_exception: OFF | ON OFF: Faulty results are rejected. ON: Results are never rejected.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:MOEXception?')
		return Conversions.str_to_bool(response)

	def set_mo_exception(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:MOEXception \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_mo_exception(meas_on_exception = False) \n
		Specifies whether measurement results identified as faulty or inaccurate are rejected. \n
			:param meas_on_exception: OFF | ON OFF: Faulty results are rejected. ON: Results are never rejected.
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:MOEXception {param}')

	def get_nvfilter(self) -> int or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:NVFilter \n
		Snippet: value: int or bool = driver.configure.nrSubMeas.multiEval.get_nvfilter() \n
		Specifies, enables or disables the number of resource blocks (NRB) view filter. If the filter is active, only slots with
		a matching number of allocated resource blocks are measured. \n
			:return: nrb_view_filter: (integer or boolean) numeric | ON | OFF Number of allocated resource blocks The allowed values depend on the SC spacing and on the channel bandwidth, see 'Resource elements, grids and blocks'. ON | OFF enables or disables the filter.
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:NVFilter?')
		return Conversions.str_to_int_or_bool(response)

	def set_nvfilter(self, nrb_view_filter: int or bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:NVFilter \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_nvfilter(nrb_view_filter = 1) \n
		Specifies, enables or disables the number of resource blocks (NRB) view filter. If the filter is active, only slots with
		a matching number of allocated resource blocks are measured. \n
			:param nrb_view_filter: (integer or boolean) numeric | ON | OFF Number of allocated resource blocks The allowed values depend on the SC spacing and on the channel bandwidth, see 'Resource elements, grids and blocks'. ON | OFF enables or disables the filter.
		"""
		param = Conversions.decimal_or_bool_value_to_str(nrb_view_filter)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:NVFilter {param}')

	# noinspection PyTypeChecker
	def get_ctv_filter(self) -> enums.ChannelTypeB:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:CTVFilter \n
		Snippet: value: enums.ChannelTypeB = driver.configure.nrSubMeas.multiEval.get_ctv_filter() \n
		No command help available \n
			:return: channel_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:CTVFilter?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelTypeB)

	def set_ctv_filter(self, channel_type: enums.ChannelTypeB) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:CTVFilter \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_ctv_filter(channel_type = enums.ChannelTypeB.OFF) \n
		No command help available \n
			:param channel_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(channel_type, enums.ChannelTypeB)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:CTVFilter {param}')

	def get_nsub_frames(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:NSUBframes \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.get_nsub_frames() \n
		Specifies the number of subframes to be evaluated. \n
			:return: no_subframe: decimal Range: 1 to 250
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:NSUBframes?')
		return Conversions.str_to_int(response)

	def set_nsub_frames(self, no_subframe: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:NSUBframes \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_nsub_frames(no_subframe = 1) \n
		Specifies the number of subframes to be evaluated. \n
			:param no_subframe: decimal Range: 1 to 250
		"""
		param = Conversions.decimal_value_to_str(no_subframe)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:NSUBframes {param}')

	# noinspection PyTypeChecker
	def get_fstructure(self) -> enums.ConfigType:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:FSTRucture \n
		Snippet: value: enums.ConfigType = driver.configure.nrSubMeas.multiEval.get_fstructure() \n
		No command help available \n
			:return: frame_structure: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:FSTRucture?')
		return Conversions.str_to_scalar_enum(response, enums.ConfigType)

	# noinspection PyTypeChecker
	def get_pformat(self) -> enums.PucchFormat:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PFORmat \n
		Snippet: value: enums.PucchFormat = driver.configure.nrSubMeas.multiEval.get_pformat() \n
		No command help available \n
			:return: pucch_format: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:PFORmat?')
		return Conversions.str_to_scalar_enum(response, enums.PucchFormat)

	def set_pformat(self, pucch_format: enums.PucchFormat) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:PFORmat \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_pformat(pucch_format = enums.PucchFormat.F1) \n
		No command help available \n
			:param pucch_format: No help available
		"""
		param = Conversions.enum_scalar_to_str(pucch_format, enums.PucchFormat)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:PFORmat {param}')

	def get_dss_pusch(self) -> int:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DSSPusch \n
		Snippet: value: int = driver.configure.nrSubMeas.multiEval.get_dss_pusch() \n
		No command help available \n
			:return: delta_seq_sh_pusch: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:DSSPusch?')
		return Conversions.str_to_int(response)

	def set_dss_pusch(self, delta_seq_sh_pusch: int) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:DSSPusch \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_dss_pusch(delta_seq_sh_pusch = 1) \n
		No command help available \n
			:param delta_seq_sh_pusch: No help available
		"""
		param = Conversions.decimal_value_to_str(delta_seq_sh_pusch)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:DSSPusch {param}')

	def get_ghopping(self) -> bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:GHOPping \n
		Snippet: value: bool = driver.configure.nrSubMeas.multiEval.get_ghopping() \n
		No command help available \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('CONFigure:NRSub:MEASurement<Instance>:MEValuation:GHOPping?')
		return Conversions.str_to_bool(response)

	def set_ghopping(self, value: bool) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:GHOPping \n
		Snippet: driver.configure.nrSubMeas.multiEval.set_ghopping(value = False) \n
		No command help available \n
			:param value: No help available
		"""
		param = Conversions.bool_to_str(value)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:GHOPping {param}')

	def clone(self) -> 'MultiEvalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiEvalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
