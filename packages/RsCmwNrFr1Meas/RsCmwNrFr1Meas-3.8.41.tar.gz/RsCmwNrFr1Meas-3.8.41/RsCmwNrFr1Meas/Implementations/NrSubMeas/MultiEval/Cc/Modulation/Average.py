from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AverageCls:
	"""Average commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tolerance: int: decimal Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits. Unit: %
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
			- Tx_Power: float: float User equipment power Unit: dBm
			- Peak_Power: float: float User equipment peak power Unit: dBm
			- Psd: float: No parameter help available
			- Evm_Dmrs_Low: float: float EVM DMRS value, low EVM window position Unit: %
			- Evm_Dmrs_High: float: float EVM DMRS value, high EVM window position Unit: %
			- Mag_Err_Dmrs_Low: float: float Magnitude error DMRS value, low EVM window position Unit: %
			- Mag_Err_Dmrs_High: float: float Magnitude error DMRS value, high EVM window position Unit: %
			- Ph_Error_Dmrs_Low: float: float Phase error DMRS value, low EVM window position Unit: deg
			- Ph_Error_Dmrs_High: float: float Phase error DMRS value, high EVM window position Unit: deg
			- Freq_Error_Ppm: float: float Carrier frequency error in ppm Unit: ppm
			- Sample_Clock_Err: float: No parameter help available
			- Carrier_Power: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
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
			ArgStruct.scalar_float('Tx_Power'),
			ArgStruct.scalar_float('Peak_Power'),
			ArgStruct.scalar_float('Psd'),
			ArgStruct.scalar_float('Evm_Dmrs_Low'),
			ArgStruct.scalar_float('Evm_Dmrs_High'),
			ArgStruct.scalar_float('Mag_Err_Dmrs_Low'),
			ArgStruct.scalar_float('Mag_Err_Dmrs_High'),
			ArgStruct.scalar_float('Ph_Error_Dmrs_Low'),
			ArgStruct.scalar_float('Ph_Error_Dmrs_High'),
			ArgStruct.scalar_float('Freq_Error_Ppm'),
			ArgStruct.scalar_float('Sample_Clock_Err'),
			ArgStruct.scalar_float('Carrier_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
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
			self.Tx_Power: float = None
			self.Peak_Power: float = None
			self.Psd: float = None
			self.Evm_Dmrs_Low: float = None
			self.Evm_Dmrs_High: float = None
			self.Mag_Err_Dmrs_Low: float = None
			self.Mag_Err_Dmrs_High: float = None
			self.Ph_Error_Dmrs_Low: float = None
			self.Ph_Error_Dmrs_High: float = None
			self.Freq_Error_Ppm: float = None
			self.Sample_Clock_Err: float = None
			self.Carrier_Power: float = None

	def read(self, carrierComponent=repcap.CarrierComponent.Default) -> ResultData:
		"""SCPI: READ:NRSub:MEASurement<Instance>:MEValuation[:CC<no>]:MODulation:AVERage \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.modulation.average.read(carrierComponent = repcap.CarrierComponent.Default) \n
		Return the current, average and standard deviation single-value results for carrier <no>. The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'READ:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:MODulation:AVERage?', self.__class__.ResultData())

	def fetch(self, carrierComponent=repcap.CarrierComponent.Default) -> ResultData:
		"""SCPI: FETCh:NRSub:MEASurement<Instance>:MEValuation[:CC<no>]:MODulation:AVERage \n
		Snippet: value: ResultData = driver.nrSubMeas.multiEval.cc.modulation.average.fetch(carrierComponent = repcap.CarrierComponent.Default) \n
		Return the current, average and standard deviation single-value results for carrier <no>. The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'FETCh:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:MODulation:AVERage?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tolerance: int: decimal Out of tolerance result, i.e. percentage of measurement intervals of the statistic count for modulation measurements exceeding the specified modulation limits. Unit: %
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
			- Tx_Power: float or bool: float User equipment power Unit: dBm
			- Peak_Power: float or bool: float User equipment peak power Unit: dBm
			- Psd: float or bool: No parameter help available
			- Evm_Dmrs_Low: float or bool: float EVM DMRS value, low EVM window position Unit: %
			- Evm_Dmrs_High: float or bool: float EVM DMRS value, high EVM window position Unit: %
			- Mag_Err_Dmrs_Low: float or bool: float Magnitude error DMRS value, low EVM window position Unit: %
			- Mag_Err_Dmrs_High: float or bool: float Magnitude error DMRS value, high EVM window position Unit: %
			- Ph_Error_Dmrs_Low: float or bool: float Phase error DMRS value, low EVM window position Unit: deg
			- Ph_Error_Dmrs_High: float or bool: float Phase error DMRS value, high EVM window position Unit: deg
			- Freq_Error_Ppm: float or bool: float Carrier frequency error in ppm Unit: ppm
			- Sample_Clock_Err: float or bool: No parameter help available
			- Carrier_Power: float or bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
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
			ArgStruct.scalar_float_ext('Tx_Power'),
			ArgStruct.scalar_float_ext('Peak_Power'),
			ArgStruct.scalar_float_ext('Psd'),
			ArgStruct.scalar_float_ext('Evm_Dmrs_Low'),
			ArgStruct.scalar_float_ext('Evm_Dmrs_High'),
			ArgStruct.scalar_float_ext('Mag_Err_Dmrs_Low'),
			ArgStruct.scalar_float_ext('Mag_Err_Dmrs_High'),
			ArgStruct.scalar_float_ext('Ph_Error_Dmrs_Low'),
			ArgStruct.scalar_float_ext('Ph_Error_Dmrs_High'),
			ArgStruct.scalar_float_ext('Freq_Error_Ppm'),
			ArgStruct.scalar_float_ext('Sample_Clock_Err'),
			ArgStruct.scalar_float_ext('Carrier_Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
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
			self.Tx_Power: float or bool = None
			self.Peak_Power: float or bool = None
			self.Psd: float or bool = None
			self.Evm_Dmrs_Low: float or bool = None
			self.Evm_Dmrs_High: float or bool = None
			self.Mag_Err_Dmrs_Low: float or bool = None
			self.Mag_Err_Dmrs_High: float or bool = None
			self.Ph_Error_Dmrs_Low: float or bool = None
			self.Ph_Error_Dmrs_High: float or bool = None
			self.Freq_Error_Ppm: float or bool = None
			self.Sample_Clock_Err: float or bool = None
			self.Carrier_Power: float or bool = None

	def calculate(self, carrierComponent=repcap.CarrierComponent.Default) -> CalculateStruct:
		"""SCPI: CALCulate:NRSub:MEASurement<Instance>:MEValuation[:CC<no>]:MODulation:AVERage \n
		Snippet: value: CalculateStruct = driver.nrSubMeas.multiEval.cc.modulation.average.calculate(carrierComponent = repcap.CarrierComponent.Default) \n
		Return the current, average and standard deviation single-value results for carrier <no>. The values described below are
		returned by FETCh and READ commands. CALCulate commands return limit check results instead, one value for each result
		listed below. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cc')
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		carrierComponent_cmd_val = self._cmd_group.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		return self._core.io.query_struct(f'CALCulate:NRSub:MEASurement<Instance>:MEValuation:CC{carrierComponent_cmd_val}:MODulation:AVERage?', self.__class__.CalculateStruct())
