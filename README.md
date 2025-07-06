# Industrial Process Layout Simulator

This project is an educational simulator that demonstrates simplified process control concepts using a configurable layout and real time PID controllers.

## Features
* YAML-driven configuration for layout and process models
* First-order and second-order process models with optional noise
* Configurable PID controllers with optional live tuning
* Simple signal generators for test input
* Alarm monitoring utilities
* Stability analyzer with basic heuristics
* PyQt dashboard with graphs and control widgets
* Layout can be saved and loaded at runtime

The project aims to evolve into a small interactive environment for teaching process control. A number of helper modules are provided to experiment with signal injection, alarm behaviour and stability checks. The GUI can be extended to allow editing the layout at runtime and to visualise multiple processes simultaneously.

This repository provides a minimal reference implementation. It is not a fully polished industrial system, but a starting point for experimentation.
