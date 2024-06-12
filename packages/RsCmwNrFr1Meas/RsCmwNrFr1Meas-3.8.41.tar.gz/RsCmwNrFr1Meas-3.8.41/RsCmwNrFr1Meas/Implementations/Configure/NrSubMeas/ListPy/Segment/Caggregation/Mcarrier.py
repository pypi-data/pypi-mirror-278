from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McarrierCls:
	"""Mcarrier commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mcarrier", core, parent)

	def set(self, meas_carrier: enums.CarrierComponent, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>:CAGGregation:MCARrier \n
		Snippet: driver.configure.nrSubMeas.listPy.segment.caggregation.mcarrier.set(meas_carrier = enums.CarrierComponent.CC1, sEGMent = repcap.SEGMent.Default) \n
		Selects a component carrier for synchronization and single-carrier measurements. \n
			:param meas_carrier: CC1 | CC2
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		param = Conversions.enum_scalar_to_str(meas_carrier, enums.CarrierComponent)
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CAGGregation:MCARrier {param}')

	# noinspection PyTypeChecker
	def get(self, sEGMent=repcap.SEGMent.Default) -> enums.CarrierComponent:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent<no>:CAGGregation:MCARrier \n
		Snippet: value: enums.CarrierComponent = driver.configure.nrSubMeas.listPy.segment.caggregation.mcarrier.get(sEGMent = repcap.SEGMent.Default) \n
		Selects a component carrier for synchronization and single-carrier measurements. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: meas_carrier: CC1 | CC2"""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:LIST:SEGMent{sEGMent_cmd_val}:CAGGregation:MCARrier?')
		return Conversions.str_to_scalar_enum(response, enums.CarrierComponent)
