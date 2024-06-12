from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FreqErrorCls:
	"""FreqError commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("freqError", core, parent)

	def set(self, frequency_error: float or bool, qam=repcap.Qam.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM<order>:FERRor \n
		Snippet: driver.configure.nrSubMeas.multiEval.limit.qam.freqError.set(frequency_error = 1.0, qam = repcap.Qam.Default) \n
		Defines an upper limit for the carrier frequency error (QAM modulations) . \n
			:param frequency_error: (float or boolean) numeric | ON | OFF Range: 0 ppm to 1 ppm, Unit: ppm ON | OFF enables or disables the limit check.
			:param qam: optional repeated capability selector. Default value: Order16 (settable in the interface 'Qam')
		"""
		param = Conversions.decimal_or_bool_value_to_str(frequency_error)
		qam_cmd_val = self._cmd_group.get_repcap_cmd_value(qam, repcap.Qam)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM{qam_cmd_val}:FERRor {param}')

	def get(self, qam=repcap.Qam.Default) -> float or bool:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM<order>:FERRor \n
		Snippet: value: float or bool = driver.configure.nrSubMeas.multiEval.limit.qam.freqError.get(qam = repcap.Qam.Default) \n
		Defines an upper limit for the carrier frequency error (QAM modulations) . \n
			:param qam: optional repeated capability selector. Default value: Order16 (settable in the interface 'Qam')
			:return: frequency_error: (float or boolean) numeric | ON | OFF Range: 0 ppm to 1 ppm, Unit: ppm ON | OFF enables or disables the limit check."""
		qam_cmd_val = self._cmd_group.get_repcap_cmd_value(qam, repcap.Qam)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIMit:QAM{qam_cmd_val}:FERRor?')
		return Conversions.str_to_float_or_bool(response)
