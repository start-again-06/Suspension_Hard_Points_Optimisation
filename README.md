# Vehicle Multi-Body Dynamics Optimization using Genetic Algorithm (GA) in MATLAB Simulink

---

## Overview
This project optimizes multi-body **vehicle dynamics** using a **Genetic Algorithm (GA)** by integrating Python with MATLAB Simulink. It automatically updates suspension parameters, runs Simulink simulations, and finds the optimal setup for improved handling, ride comfort, and stability.

---

## Key Features
- **Automated Parameter Tuning:** Optimizes spring stiffness, damping ratio, and roll center height  
- **Python-MATLAB Simulink Integration:** Updates Simulink `.mat` files and runs simulations using `matlab.engine`  
- **Simulation-Based Evaluation:** Extracts key performance metrics (Body Roll, Camber Gain)  
- **Visualization:** Compares original vs optimized suspension parameters in bar charts  
- **Scalable & Extensible:** Can adapt to additional vehicle dynamics parameters (Caster, Toe, Ackermann %)  

---

## How It Works
- Reads suspension parameters from `suspension_params.mat`  
- Runs Simulink simulation using MATLAB Engine API  
- Extracts key performance metrics (Body Roll, Camber Gain)  
- Uses Genetic Algorithm (GA) to optimize suspension parameters  
- Compares and visualizes results (Initial vs Optimized setup)  

---

## Optimization Results
- Generates optimized suspension parameter comparison plots (Original vs Optimized setup)  
- Provides MATLAB simulation logs for performance review  

---

## License
MIT License. Free to use, modify, and distribute for academic and research purposes.

