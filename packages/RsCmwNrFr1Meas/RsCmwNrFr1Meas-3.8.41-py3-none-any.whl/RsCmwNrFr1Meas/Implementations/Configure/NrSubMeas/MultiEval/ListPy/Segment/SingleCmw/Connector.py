from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConnectorCls:
	"""Connector commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connector", core, parent)

	def set(self, cmws_connector: enums.CmwsConnector, sEGMent=repcap.SEGMent.Default) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:CMWS:CONNector \n
		Snippet: driver.configure.nrSubMeas.multiEval.listPy.segment.singleCmw.connector.set(cmws_connector = enums.CmwsConnector.R11, sEGMent = repcap.SEGMent.Default) \n
		Selects the RF input connector for segment <no> for the connector mode LIST, see method RsCmwNrFr1Meas.Configure.
		NrSubMeas.MultiEval.ListPy.SingleCmw.cmode. All segments of a list mode measurement must use connectors of the same bench.
		For possible connector values, see 'Values for RF path selection'. \n
			:param cmws_connector: Selects the input connector
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		param = Conversions.enum_scalar_to_str(cmws_connector, enums.CmwsConnector)
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:CMWS:CONNector {param}')

	# noinspection PyTypeChecker
	def get(self, sEGMent=repcap.SEGMent.Default) -> enums.CmwsConnector:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent<no>:CMWS:CONNector \n
		Snippet: value: enums.CmwsConnector = driver.configure.nrSubMeas.multiEval.listPy.segment.singleCmw.connector.get(sEGMent = repcap.SEGMent.Default) \n
		Selects the RF input connector for segment <no> for the connector mode LIST, see method RsCmwNrFr1Meas.Configure.
		NrSubMeas.MultiEval.ListPy.SingleCmw.cmode. All segments of a list mode measurement must use connectors of the same bench.
		For possible connector values, see 'Values for RF path selection'. \n
			:param sEGMent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:return: cmws_connector: Selects the input connector"""
		sEGMent_cmd_val = self._cmd_group.get_repcap_cmd_value(sEGMent, repcap.SEGMent)
		response = self._core.io.query_str(f'CONFigure:NRSub:MEASurement<Instance>:MEValuation:LIST:SEGMent{sEGMent_cmd_val}:CMWS:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.CmwsConnector)
