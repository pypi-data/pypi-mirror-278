from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPyCls:
	"""ListPy commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("listPy", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ListMode:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:LIST:MODE \n
		Snippet: value: enums.ListMode = driver.trigger.nrSubMeas.listPy.get_mode() \n
		Specifies the trigger mode for list mode measurements. For configuration of retrigger flags, see method RsCmwNrFr1Meas.
		Configure.NrSubMeas.ListPy.Segment.Setup.set. For configuration of the global trigger source, see method RsCmwNrFr1Meas.
		Trigger.NrSubMeas.MultiEval.source. \n
			:return: mode: ONCE | SEGMent ONCE A trigger event is only required to start the measurement. The entire range of segments to be measured is captured without additional trigger event. The global trigger source is used. SEGMent The retrigger flag of each segment is evaluated. It defines whether a trigger event is required and which trigger source is used.
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:LIST:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ListMode)

	def set_mode(self, mode: enums.ListMode) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:LIST:MODE \n
		Snippet: driver.trigger.nrSubMeas.listPy.set_mode(mode = enums.ListMode.ONCE) \n
		Specifies the trigger mode for list mode measurements. For configuration of retrigger flags, see method RsCmwNrFr1Meas.
		Configure.NrSubMeas.ListPy.Segment.Setup.set. For configuration of the global trigger source, see method RsCmwNrFr1Meas.
		Trigger.NrSubMeas.MultiEval.source. \n
			:param mode: ONCE | SEGMent ONCE A trigger event is only required to start the measurement. The entire range of segments to be measured is captured without additional trigger event. The global trigger source is used. SEGMent The retrigger flag of each segment is evaluated. It defines whether a trigger event is required and which trigger source is used.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ListMode)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:LIST:MODE {param}')

	# noinspection PyTypeChecker
	def get_nbandwidth(self) -> enums.NbTrigger:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:LIST:NBANdwidth \n
		Snippet: value: enums.NbTrigger = driver.trigger.nrSubMeas.listPy.get_nbandwidth() \n
		Selects the trigger evaluation bandwidth for the retrigger source IFPNarrowband. Select the retrigger source via method
		RsCmwNrFr1Meas.Configure.NrSubMeas.ListPy.Segment.Setup.set. \n
			:return: nbandwidth: M010 | M020 | M040 | M080 Evaluation bandwidth 10 MHz to 80 MHz
		"""
		response = self._core.io.query_str('TRIGger:NRSub:MEASurement<Instance>:LIST:NBANdwidth?')
		return Conversions.str_to_scalar_enum(response, enums.NbTrigger)

	def set_nbandwidth(self, nbandwidth: enums.NbTrigger) -> None:
		"""SCPI: TRIGger:NRSub:MEASurement<Instance>:LIST:NBANdwidth \n
		Snippet: driver.trigger.nrSubMeas.listPy.set_nbandwidth(nbandwidth = enums.NbTrigger.M010) \n
		Selects the trigger evaluation bandwidth for the retrigger source IFPNarrowband. Select the retrigger source via method
		RsCmwNrFr1Meas.Configure.NrSubMeas.ListPy.Segment.Setup.set. \n
			:param nbandwidth: M010 | M020 | M040 | M080 Evaluation bandwidth 10 MHz to 80 MHz
		"""
		param = Conversions.enum_scalar_to_str(nbandwidth, enums.NbTrigger)
		self._core.io.write(f'TRIGger:NRSub:MEASurement<Instance>:LIST:NBANdwidth {param}')
