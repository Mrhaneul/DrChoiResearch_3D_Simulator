Two-Charge Gravity & Gravitational Lensing Simulator
Overview

This repository contains a computational and visualization framework for exploring a Two-Charge Theory of Gravity (TCG) and its observable consequences, particularly gravitational lensing and large-scale cosmic dynamics.

The project builds on the theoretical work presented in Ye Jin Han, “A Two-Charge Theory of Gravity” (2018) 

Honors Thesis_YeJin_Han

 and extends it through modern 3D simulations implemented using Manim Community (Python). The simulations visualize how light particles propagate through space influenced by gravitating and anti-gravitating mass sources, offering intuition for repulsive gravity, inverted lensing, and cosmological expansion effects.

This repository is part of an ongoing research collaboration under Dr. Hyung S. Choi, with the long-term objective of refining, validating, and communicating the physical implications of the TCG framework.

Theoretical Background: Two-Charge Gravity (TCG)
Motivation

Standard gravitational theory struggles to fully explain several major cosmological observations, including:

Accelerating expansion of the universe (dark energy)

Matter–antimatter (baryonic) asymmetry

Dark matter distribution inferred from gravitational lensing

Early-universe inflation

The Two-Charge Theory of Gravity proposes that gravity is not mono-charged but instead possesses two gravitational charges, analogous to electric charge:

Like gravitational charges attract

Opposite gravitational charges repel

This differs fundamentally from electromagnetism and introduces repulsive gravitational interactions without modifying local Newtonian or General Relativistic behavior.

Key Results from the Thesis

Ye Jin Han’s thesis demonstrates that:

A 3D alternating lattice of positive and negative gravitational charges produces a non-zero net repulsive force at any arbitrary point.

Large-scale repulsion naturally emerges even when local interactions remain attractive.

A decreasing matter–antimatter ratio over distance leads to locally attractive gravity, explaining why antigravity is not observed in everyday physics.

The framework can account for:

Inflation

Dark energy as residual repulsive gravity

Inverted gravitational lensing

Matter–antimatter separation over cosmic time

These results motivate visual simulations to explore how light and test particles behave under TCG.

What This Repository Does

This repository provides:

3D gravitational lensing simulations

Dynamic light-particle propagation

Multiple gravity and antigravity sources

Time-evolving particle trajectories

Visual intuition for repulsive vs. attractive gravity

The simulations are not merely animations, they are computational experiments designed to reflect the qualitative predictions of TCG.

Simulation Highlights
Multi-Source Gravity & Antigravity

Supports multiple gravitating and anti-gravitating sources placed arbitrarily in 3D space.

Sources may be layered, clustered, or symmetrically arranged.

Each source contributes to the net force field acting on light particles.

Light Particle Dynamics

Light rays are modeled as discrete particles with velocity vectors.

At each timestep, particles experience cumulative gravitational influence.

Trajectories bend toward gravitating sources and away from anti-gravitating sources.

Demonstrates:

Standard lensing

Inverted lensing

Deflection voids (“dark spots”)

Visualization Engine

Built on Manim Community (v0.19+)

Fully 3D camera control

Real-time trajectory rendering

Scalable to hundreds or thousands of particles

Repository Structure (Typical)
.
├── simulator/
│   ├── light3d.py               # Light particle physics
│   ├── gravity_source3d.py      # Positive gravity sources
│   ├── antigravity_source3d.py  # Negative gravity sources
│   ├── control_panel.py         # Simulation parameters
│
├── scenes/
│   ├── multi_grav.py            # Main 3D scene (TestMultiGrav)
│
├── videos/
│   ├── *.mp4                    # Rendered simulation outputs
│
├── README.md
└── requirements.txt


(Exact structure may evolve as the project expands.)

Example Simulation

To render a multi-source gravitational lensing scene:

python -m manim -pqh scenes/multi_grav.py TestMultiGrav


Options:

-p : Preview after rendering

-q h : High quality

--disable_caching : Recommended for large particle counts

Scientific Interpretation

The simulations visually demonstrate several predictions of TCG:

Repulsive background gravity emerging from mixed-charge distributions

Stable local attraction after charge segregation

Inverted lensing consistent with dark-matter-like observations

Cosmic acceleration without introducing an ad-hoc cosmological constant

These visual tools complement analytic lattice calculations and serve as an exploratory bridge between theory and observation.

Current Status

Core simulation engine implemented

Multi-gravity source support complete

Light-particle dynamics stable

3D rendering pipeline functional

Ongoing performance optimization for large particle counts

Future Work

Planned or proposed extensions include:

GPU acceleration for million-particle simulations

Continuous density fields instead of point sources

Time-evolving charge ratios (cosmological epochs)

Quantitative lensing comparison with DES / ΛCDM maps

Integration with observational datasets

Publication-grade figures and animations

Credits & Acknowledgements

Dr. Hyung S. Choi — Project Supervisor, Two-Charge Gravity Theory

Ye Jin Han — Foundational theoretical work and lattice simulations

Haneul Kim — 3D simulation design, Manim implementation, visualization

Inspired by lattice summation methods analogous to the Madelung constant

License

This repository is intended for academic and research use.
License details may be added upon publication or broader release.

Citation

If you use or reference this work, please cite:

Ye Jin Han, A Two-Charge Theory of Gravity, Honors Thesis, Greenville University, 2018.
