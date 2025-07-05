import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from src.signal_generator import SignalGenerator, SignalConfig
from src.alarm_monitor import AlarmMonitor, AlarmConfig


def test_signal_generator_sine():
    gen = SignalGenerator(SignalConfig(type="sine", amplitude=1.0, frequency=0.5, offset=0.0))
    val1 = gen.value(0.0)
    val2 = gen.value(0.5)
    assert abs(val1) < 1e-6
    assert abs(val2) == 1.0


def test_alarm_monitor():
    alarm = AlarmMonitor(AlarmConfig(low=0, high=5))
    assert not alarm.update(2)
    assert alarm.update(6)