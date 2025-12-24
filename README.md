# Two-Charge Gravity & Gravitational Lensing Simulator

## Overview

This repository contains a computational and visualization framework for exploring a **Two-Charge Theory of Gravity (TCG)** and its implications for gravitational lensing, cosmic expansion, and large-scale structure formation.

The project builds on the theoretical foundation established in **Ye Jin Han’s honors thesis, _A Two-Charge Theory of Gravity_ (2018)** and extends it through modern **3D simulations using Manim (Python)**. These simulations visualize the behavior of light particles under the influence of both **gravitating and anti-gravitating mass sources**, providing physical intuition for repulsive gravity and inverted gravitational lensing.

This work is part of an ongoing research effort under the supervision of **Dr. Hyung S. Choi**.

---

## Theoretical Background

### Two-Charge Theory of Gravity (TCG)

Unlike the standard mono-charged model of gravity, TCG proposes that gravity possesses **two distinct gravitational charges**:

- Like gravitational charges **attract**
- Opposite gravitational charges **repel**

This framework naturally introduces repulsive gravitational interactions while remaining consistent with known local gravitational physics.

Key motivations for TCG include explaining:

- Accelerating expansion of the universe (dark energy)
- Matter–antimatter (baryonic) asymmetry
- Dark matter–like gravitational lensing effects
- Early-universe inflation

Large-scale lattice simulations in the original thesis demonstrate that a universe with alternating gravitational charges produces a **net repulsive force**, even when local interactions remain attractive.

---

## Purpose of This Repository

This repository focuses on **visual and computational exploration** of TCG predictions by:

- Simulating light-particle trajectories in 3D space
- Modeling multiple gravitating and anti-gravitating sources
- Visualizing gravitational and inverted gravitational lensing
- Providing intuition for repulsive gravity at cosmological scales

These simulations serve as qualitative experiments that complement analytic lattice models.

---

## Features

- 3D gravitational lensing simulations
- Multiple gravity and antigravity sources
- Dynamic light-particle propagation
- Time-evolving trajectories
- Manim-based rendering with full camera control
- Modular physics and visualization components

---

## Repository Structure
(The exact structure may evolve as the project develops.)

```
.
├── simulator/
│   ├── light3d.py               # Light particle dynamics
│   ├── gravity_source3d.py      # Gravitating mass sources
│   ├── antigravity_source3d.py  # Anti-gravitating mass sources
│   ├── control_panel.py         # Simulation parameters
│
├── scenes/
│   ├── multi_grav.py            # Main Manim scene (TestMultiGrav)
│
├── videos/
│   ├── *.mp4                    # Rendered simulation outputs
│
├── README.md
└── requirements.txt
```

# Simulation Guide and Project Status

## Running a Simulation

To render a simulation using **Manim**, run the following command from the project root:

```bash
python -m manim -pqh scenes/multi_grav.py TestMultiGrav
```

### Options

- `-p` : Preview the video after rendering  
- `-q h` : High-quality render  
- `--disable_caching` : Recommended for large scenes with many objects  

---

## Simulation Videos

_Add rendered outputs, links, or GIFs here._

### Example Simulations

#### Multi-source gravitational lensing

- **Description**:  
  Light particles propagating through a field of multiple gravitating and anti-gravitating sources.

- **Video**:  
  https://youtu.be/fBuN99ohgHY
  
  https://youtu.be/jxYMFTuZRpY
  
  https://youtu.be/b3LoGl2RoXQ
  

#### Inverted gravitational lensing

- **Description**:  
  Light bending away from anti-gravitating mass distributions.

- **Video**:  
  *(add link or file path here)*

You may embed videos as links, GitHub-hosted MP4 files, or external links (e.g., Google Drive, YouTube).

---

## Scientific Interpretation

The simulations demonstrate several qualitative predictions of the **Two-Charge Gravity** framework:

- Emergent large-scale repulsive gravity  
- Local attractive gravity after charge segregation  
- Inverted gravitational lensing consistent with dark matter–like observations  
- Accelerated expansion without invoking an ad hoc cosmological constant  

These results provide visual support for theoretical lattice calculations.

---

## Current Status

- Core simulation engine implemented  
- Multi-source gravity and antigravity supported  
- Light-particle dynamics stable  
- 3D rendering pipeline functional  
- Performance optimizations ongoing for large particle counts  

---

## Future Work

Planned extensions include:

- GPU acceleration for large-scale simulations  
- Continuous mass-density fields  
- Time-evolving charge ratios (cosmological epochs)  
- Quantitative lensing comparisons with observational data  
- Publication-grade figures and animations  

---

## Acknowledgements

- **Dr. Hyung S. Choi** — Project supervisor and originator of the Two-Charge Gravity framework  
- **Ye Jin Han** — Foundational theoretical and lattice simulation work  
- **Kip Park** — Initial development of the 2D gravitational lensing simulation using **pygame** and **NumPy**, which established the conceptual and computational groundwork for this project  

---

## Citation

If you use or reference this work, please cite:

> Ye Jin Han, *A Two-Charge Theory of Gravity*, Honors Thesis, Greenville University, 2018.
