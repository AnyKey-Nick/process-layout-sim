import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import math

from src.pid_controller import PIDConfig, PIDController


def test_pid_converges_to_setpoint():
    cfg = PIDConfig(Kp=1.0, Ki=0.2, Kd=0.0, setpoint=1.0, output_limits=(-10, 10))
    pid = PIDController(cfg)
    value = 0.0
    for _ in range(1000):
        u = pid.compute(value, 0.1)
        # simple first order system approximation
        value += 0.5 * (u - value) * 0.1
    assert math.isclose(value, 1.0, rel_tol=1e-2, abs_tol=1e-2)