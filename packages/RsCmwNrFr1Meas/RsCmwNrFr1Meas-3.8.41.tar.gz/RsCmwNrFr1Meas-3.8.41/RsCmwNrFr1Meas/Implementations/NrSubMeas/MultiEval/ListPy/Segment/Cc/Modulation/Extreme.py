from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExtremeCls:
	"""Extreme commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("extreme", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Seg_Reliability: int: decimal Reliability indicator for the segment
			- Statist_Expired: int: decimal Reached statistical length in slots
			- Out_Of_Tolerance: int: decimal Percentage of measured subframes with failed limit check Unit: %
			- Evm_Rms_Low: float: float EVM RMS value, low EVM window position Unit: %
			- Evm_Rms_High: float: float EVM RMS value, high EVM window position Unit: %
			- Evm_Peak_Low: float: float EVM peak value, low EVM window position Unit: %
			- Evm_Peak_High: float: float EVM peak value, high EVM window position Unit: %
			- Mag_Error_Rms_Low: float: float Magnitude error RMS value, low EVM window position Unit: %
			- Mag_Error_Rms_High: float: float Magnitude error RMS value, low EVM window position Unit: %
			- Mag_Error_Peak_Low: float: float Magnitude error peak value, low EVM window position Unit: %
			- Mag_Err_Peak_High: float: float Magnitude error peak value, high EVM window position Unit: %
			- Ph_Error_Rms_Low: float: float Phase error RMS value, low EVM window position Unit: deg
			- Ph_Error_Rms_High: float: float Phase error RMS value, high EVM window position Unit: deg
			- Ph_Error_Peak_Low: float: float Phase error peak value, low EVM window position Unit: deg
			- Ph_Error_Peak_High: float: float Phase error peak value, high EVM window position Unit: deg
			- Iq_Offset: float: float I/Q origin offset Unit: dBc
			- Frequency_Error: float: float Carrier frequency error Unit: Hz
			- Timing_Error: float: float Time error Unit: Ts (basic time unit)
			- Tx_Power_Minimum: float: float Minimum user equipment power Unit: dBm
			- Tx_Power_Maximum: float: No parameter help available
			- Peak_Power_Min: float: float Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Peak_Power_Max: float: float Maximum user equipment peak power Unit: dBm
			- Psd_Minimum: float: No parameter help available
			- Psd_Maximum: float: No parameter help available
			- Evm_Dmrs_Low: float: float EVM DMRS value, low EVM window position Unit: %
			- Evm_Dmrs_High: float: float EVM DMRS value, high EVM window position Unit: %
			- Mag_Err_Dmrs_Low: float: float Magnitude error DMRS value, low EVM window position Unit: %
			- Mag_Err_Dmrs_High: float: float Magnitude error DMRS value, high EVM window position Unit: %
			- Ph_Error_Dmrs_Low: float: float Phase error DMRS value, low EVM window position Unit: deg
			- Ph_Error_Dmrs_High: float: float Phase error DMRS value, high EVM window position Unit: deg"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float('Evm_Rms_Low'),
			ArgStruct.scalar_float('Evm_Rms_High'),
			ArgStruct.scalar_float('Evm_Peak_Low'),
			ArgStruct.scalar_float('Evm_Peak_High'),
			ArgStruct.scalar_float('Mag_Error_Rms_Low'),
			ArgStruct.scalar_float('Mag_Error_Rms_High'),
			ArgStruct.scalar_float('Mag_Error_Peak_Low'),
			ArgStruct.scalar_float('Mag_Err_Peak_High'),
			ArgStruct.scalar_float('Ph_Error_Rms_Low'),
			ArgStruct.scalar_float('Ph_Error_Rms_High'),
			ArgStruct.scalar_float('Ph_Error_Peak_Low'),
			ArgStruct.scalar_float('Ph_Error_Peak_High'),
			ArgStruct.scalar_float('Iq_Offset'),
			ArgStruct.scalar_float('Frequency_Error'),
			ArgStruct.scalar_float('Timing_Error'),
			ArgStruct.scalar_float('Tx_Power_Minimum'),
			ArgStruct.scalar_float('Tx_Power_Maximum'),
			ArgStruct.scalar_float('Peak_Power_Min'),
			ArgStruct.scalar_float('Peak_Power_Max'),
			ArgStruct.scalar_float('Psd_Minimum'),
			ArgStruct.scalar_float('Psd_Maximum'),
			ArgStruct.scalar_float('Evm_Dmrs_Low'),
			ArgStruct.scalar_float('Evm_Dmrs_High'),
			ArgStruct.scalar_float('Mag_Err_Dmrs_Low'),
			ArgStruct.scalar_float('Mag_Err_Dmrs_High'),
			ArgStruct.scalar_float('Ph_Error_Dmrs_Low'),
			ArgStruct.scalar_float('Ph_Error_Dmrs_High')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Evm_Rms_Low: float = None
			self.Evm_Rms_High: float = None
			self.Evm_Peak_Low: float = None
			self.Evm_Peak_High: float = None
			self.Mag_Error_Rms_Low: float = None
			self.Mag_Error_Rms_High: float = None
			self.Mag_Error_Peak_Low: float = None
			self.Mag_Err_Peak_High: float = None
			self.Ph_Error_Rms_Low: float = None
			self.Ph_Error_Rms_High: float = None
			self.Ph_Error_Peak_Low: float = None
			self.Ph_Error_Peak_High: float = None
			self.Iq_Offset: float = None
			self.Frequency_Error: float = None
			self.Timing_Error: float = None
			self.Tx_Power_Minimum: float = None
			self.Tx_Power_Maximum: float = None
			self.Peak_Power_Min: float = None
			self.Peak_Power_Max: float = None
			self.Psd_Minimum: float = None
			self.Psd_Maximum: float = None
			self.Evm_Dmrs_Low: float = None
			self.Evm_Dmrs_High: float = None
			self.Mag_Err_Dmrs_Low: float = None
			self.Mag_Err_Dmrs_High: float = None
			self.Ph_Error_Dmrs_Low: float = None
			self.Ph_Error_Dmrs_High: float = None

	def fetch(self, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default) -> FetchStruct:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:CC<Carrier>]:MODulation:EXTReme \n
		Snippet: value: FetchStruct = driver.nrSubMeas.multiEval.listPy.segment.cc.modulation.extreme.fetch(sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Return modulation single-value results for segment <no> in list mode, for carrier <c>. The values described below are
		returned by FETCh commands. The first four values (reliability to out of tolerance result) are also returned by CALCulate
		commands. The remaining values returned by CALCulate commands are limit check results, one value for each result listed
		below. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:MODulation:EXTReme?', self.__class__.FetchStruct())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Seg_Reliability: int: decimal Reliability indicator for the segment
			- Statist_Expired: int: decimal Reached statistical length in slots
			- Out_Of_Tolerance: int: decimal Percentage of measured subframes with failed limit check Unit: %
			- Evm_Rms_Low: float or bool: float EVM RMS value, low EVM window position Unit: %
			- Evm_Rms_High: float or bool: float EVM RMS value, high EVM window position Unit: %
			- Evm_Peak_Low: float or bool: float EVM peak value, low EVM window position Unit: %
			- Evm_Peak_High: float or bool: float EVM peak value, high EVM window position Unit: %
			- Mag_Error_Rms_Low: float or bool: float Magnitude error RMS value, low EVM window position Unit: %
			- Mag_Error_Rms_High: float or bool: float Magnitude error RMS value, low EVM window position Unit: %
			- Mag_Error_Peak_Low: float or bool: float Magnitude error peak value, low EVM window position Unit: %
			- Mag_Err_Peak_High: float or bool: float Magnitude error peak value, high EVM window position Unit: %
			- Ph_Error_Rms_Low: float or bool: float Phase error RMS value, low EVM window position Unit: deg
			- Ph_Error_Rms_High: float or bool: float Phase error RMS value, high EVM window position Unit: deg
			- Ph_Error_Peak_Low: float or bool: float Phase error peak value, low EVM window position Unit: deg
			- Ph_Error_Peak_High: float or bool: float Phase error peak value, high EVM window position Unit: deg
			- Iq_Offset: float or bool: float I/Q origin offset Unit: dBc
			- Frequency_Error: float or bool: float Carrier frequency error Unit: Hz
			- Timing_Error: float or bool: float Time error Unit: Ts (basic time unit)
			- Tx_Power_Minimum: float or bool: float Minimum user equipment power Unit: dBm
			- Tx_Power_Maximum: float or bool: No parameter help available
			- Peak_Power_Min: float or bool: float Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Peak_Power_Max: float or bool: float Maximum user equipment peak power Unit: dBm
			- Psd_Minimum: float or bool: No parameter help available
			- Psd_Maximum: float or bool: No parameter help available
			- Evm_Dmrs_Low: float or bool: float EVM DMRS value, low EVM window position Unit: %
			- Evm_Dmrs_High: float or bool: float EVM DMRS value, high EVM window position Unit: %
			- Mag_Err_Dmrs_Low: float or bool: float Magnitude error DMRS value, low EVM window position Unit: %
			- Mag_Err_Dmrs_High: float or bool: float Magnitude error DMRS value, high EVM window position Unit: %
			- Ph_Error_Dmrs_Low: float or bool: float Phase error DMRS value, low EVM window position Unit: deg
			- Ph_Error_Dmrs_High: float or bool: float Phase error DMRS value, high EVM window position Unit: deg"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Seg_Reliability'),
			ArgStruct.scalar_int('Statist_Expired'),
			ArgStruct.scalar_int('Out_Of_Tolerance'),
			ArgStruct.scalar_float_ext('Evm_Rms_Low'),
			ArgStruct.scalar_float_ext('Evm_Rms_High'),
			ArgStruct.scalar_float_ext('Evm_Peak_Low'),
			ArgStruct.scalar_float_ext('Evm_Peak_High'),
			ArgStruct.scalar_float_ext('Mag_Error_Rms_Low'),
			ArgStruct.scalar_float_ext('Mag_Error_Rms_High'),
			ArgStruct.scalar_float_ext('Mag_Error_Peak_Low'),
			ArgStruct.scalar_float_ext('Mag_Err_Peak_High'),
			ArgStruct.scalar_float_ext('Ph_Error_Rms_Low'),
			ArgStruct.scalar_float_ext('Ph_Error_Rms_High'),
			ArgStruct.scalar_float_ext('Ph_Error_Peak_Low'),
			ArgStruct.scalar_float_ext('Ph_Error_Peak_High'),
			ArgStruct.scalar_float_ext('Iq_Offset'),
			ArgStruct.scalar_float_ext('Frequency_Error'),
			ArgStruct.scalar_float_ext('Timing_Error'),
			ArgStruct.scalar_float_ext('Tx_Power_Minimum'),
			ArgStruct.scalar_float_ext('Tx_Power_Maximum'),
			ArgStruct.scalar_float_ext('Peak_Power_Min'),
			ArgStruct.scalar_float_ext('Peak_Power_Max'),
			ArgStruct.scalar_float_ext('Psd_Minimum'),
			ArgStruct.scalar_float_ext('Psd_Maximum'),
			ArgStruct.scalar_float_ext('Evm_Dmrs_Low'),
			ArgStruct.scalar_float_ext('Evm_Dmrs_High'),
			ArgStruct.scalar_float_ext('Mag_Err_Dmrs_Low'),
			ArgStruct.scalar_float_ext('Mag_Err_Dmrs_High'),
			ArgStruct.scalar_float_ext('Ph_Error_Dmrs_Low'),
			ArgStruct.scalar_float_ext('Ph_Error_Dmrs_High')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Seg_Reliability: int = None
			self.Statist_Expired: int = None
			self.Out_Of_Tolerance: int = None
			self.Evm_Rms_Low: float or bool = None
			self.Evm_Rms_High: float or bool = None
			self.Evm_Peak_Low: float or bool = None
			self.Evm_Peak_High: float or bool = None
			self.Mag_Error_Rms_Low: float or bool = None
			self.Mag_Error_Rms_High: float or bool = None
			self.Mag_Error_Peak_Low: float or bool = None
			self.Mag_Err_Peak_High: float or bool = None
			self.Ph_Error_Rms_Low: float or bool = None
			self.Ph_Error_Rms_High: float or bool = None
			self.Ph_Error_Peak_Low: float or bool = None
			self.Ph_Error_Peak_High: float or bool = None
			self.Iq_Offset: float or bool = None
			self.Frequency_Error: float or bool = None
			self.Timing_Error: float or bool = None
			self.Tx_Power_Minimum: float or bool = None
			self.Tx_Power_Maximum: float or bool = None
			self.Peak_Power_Min: float or bool = None
			self.Peak_Power_Max: float or bool = None
			self.Psd_Minimum: float or bool = None
			self.Psd_Maximum: float or bool = None
			self.Evm_Dmrs_Low: float or bool = None
			self.Evm_Dmrs_High: float or bool = None
			self.Mag_Err_Dmrs_Low: float or bool = None
			self.Mag_Err_Dmrs_High: float or bool = None
			self.Ph_Error_Dmrs_Low: float or bool = None
			self.Ph_Error_Dmrs_High: float or bool = None

	def calculate(self, sEGMent=repcap.SEGMent.Default, carrierComponent=repcap.CarrierComponent.Default) -> CalculateStruct:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<nr>[:CC<Carrier>]:MODulation:EXTReme \n
		Snippet: value: CalculateStruct = driver.nrSubMeas.multiEval.listPy.segment.cc.modulation.extreme.calculate(sEGMent = repcap.SEGMent.Default, carrierComponent = repcap.CarrierComponent.Default) \n
		Return modulation single-value results for segment <no> in list mode, for carrier <c>. The values described below are
		returned by FETCh commands. The first four values (reliability to out of tolerance result) are also returned by CALCulate
		commands. The remaining values returned by CALCulate commands are limit check results, one value for each result listed
		below. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:CC{carrierComponent_cmd_val}:MODulation:EXTReme?', self.__class__.CalculateStruct())
