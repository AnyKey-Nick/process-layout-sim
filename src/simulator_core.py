from __future__ import annotations

import time
from typing import Dict

import yaml

from .pid_controller import PIDConfig, PIDController
from .process_model import create_process, ProcessModel
from .signal_generator import SignalConfig, SignalGenerator
from .alarm_monitor import AlarmConfig, AlarmMonitor


class Simulator:
    def __init__(self, process_cfg_path: str):
        with open(process_cfg_path, 'r', encoding='utf-8') as fh:
            cfg = yaml.safe_load(fh)
        self.processes: Dict[str, ProcessModel] = {}
        self.controllers: Dict[str, PIDController] = {}
        self.signals: Dict[str, SignalGenerator] = {}
        self.alarms: Dict[str, AlarmMonitor] = {}
        for item in cfg.get('processes', []):
            name = item['name']
            model_name = item['model']
            parameters = item.get('parameters', {})
            initial = item.get('initial_value', 0.0)
            proc = create_process(model_name, parameters, initial)
            self.processes[name] = proc
            ctrl_cfg = item.get('controller')
            if ctrl_cfg:
                pid_cfg = PIDConfig(
                    Kp=ctrl_cfg.get('Kp', 0.0),
                    Ki=ctrl_cfg.get('Ki', 0.0),
                    Kd=ctrl_cfg.get('Kd', 0.0),
                    setpoint=ctrl_cfg.get('setpoint', 0.0),
                    output_limits=tuple(ctrl_cfg.get('output_limits', (0.0, 1.0))),
                )
                self.controllers[name] = PIDController(pid_cfg)
            sig_cfg = item.get('signal')
            if sig_cfg:
                self.signals[name] = SignalGenerator(SignalConfig(**sig_cfg))
            alarm_cfg = item.get('alarm')
            if alarm_cfg:
                self.alarms[name] = AlarmMonitor(AlarmConfig(**alarm_cfg))
        self.last_time = time.time()

    def step(self, dt: float | None = None) -> Dict[str, float]:
        now = time.time()
        if dt is None:
            dt = now - self.last_time
        self.last_time = now
        outputs: Dict[str, float] = {}
        t = now
        for name, proc in self.processes.items():
            ctrl = self.controllers.get(name)
            u = 0.0
            if ctrl:
                u = ctrl.compute(proc.state.value, dt)
            signal = self.signals.get(name)
            if signal:
                u += signal.value(t)
            value = proc.update(u, dt)
            alarm = self.alarms.get(name)
            if alarm:
                alarm.check(value)
            outputs[name] = value
        return outputs
