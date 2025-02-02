import numpy as np
import pandas as pd
import subprocess
import random
import scipy.io
import matlab.engine
import os
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms


eng = matlab.engine.start_matlab()


def load_suspension_data(file_path):
    return pd.read_csv(file_path)

def generate_simulink_input(params, mat_file):
    spring_stiffness, damping_ratio, roll_center_height = params

    mat_data = scipy.io.loadmat(mat_file)

    mat_data['Spring_Stiffness'] = np.array([spring_stiffness])
    mat_data['Damping_Ratio'] = np.array([damping_ratio])
    mat_data['Roll_Center_Height'] = np.array([roll_center_height])

 
    scipy.io.savemat(mat_file, mat_data)


def run_simulink_model(simulink_model, mat_file):
    try:
        eng.workspace['mat_file'] = mat_file  # Load the MAT file into MATLAB workspace
        eng.eval(f"load(mat_file)", nargout=0)  # Load the parameters in MATLAB
        eng.eval(f"sim('{simulink_model}')", nargout=0)  # Run the Simulink model
        return True
    except Exception as e:
        print(f"Error running Simulink model: {e}")
        return False


def extract_simulation_results():
    try:
        body_roll = eng.workspace['Body_Roll']  # Extract body roll variable from MATLAB
        camber_gain = eng.workspace['Camber_Gain']  # Extract camber gain variable
        return np.mean(body_roll), np.mean(camber_gain)
    except KeyError:
        print("Simulation results not found in MATLAB workspace.")
        return float("inf"), float("inf")

def fitness_function(individual):
    spring_stiffness, damping_ratio, roll_center_height = individual
    mat_file = "suspension_params.mat"
    simulink_model = "Vehicle_Suspension_Model"

 
    generate_simulink_input(individual, mat_file)
    

    success = run_simulink_model(simulink_model, mat_file)
    if not success:
        return (float("inf"),)  # Large penalty if simulation fails


    body_roll, camber_gain = extract_simulation_results()

    cost = abs(body_roll - 2.0) + abs(camber_gain - 1.5)

    return (cost,)


def optimize_vehicle_dynamics_ga():
    # GA Parameter Bounds
    spring_stiffness_range = (50, 300)
    damping_ratio_range = (0.1, 1.5)
    roll_center_height_range = (30, 70)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimize cost
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_spring", random.uniform, *spring_stiffness_range)
    toolbox.register("attr_damping", random.uniform, *damping_ratio_range)
    toolbox.register("attr_roll_center", random.uniform, *roll_center_height_range)

    toolbox.register("individual", tools.initCycle, creator.Individual, 
                     (toolbox.attr_spring, toolbox.attr_damping, toolbox.attr_roll_center), n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", fitness_function)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)  # Crossover
    toolbox.register("mutate", tools.mutPolynomialBounded, low=[50, 0.1, 30], up=[300, 1.5, 70], eta=1.0, indpb=0.2)  # Mutation
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=20)  # Population size
    ngen = 10  # Number of generations
    cxpb = 0.5  # Crossover probability
    mutpb = 0.2  # Mutation probability


    algorithms.eaSimple(population, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen, verbose=True)

 
    best_individual = tools.selBest(population, k=1)[0]
    return best_individual


def plot_results(original_params, optimized_params):
    labels = ['Spring Stiffness', 'Damping Ratio', 'Roll Center Height']
    x = np.arange(len(labels))
    
    plt.bar(x - 0.2, original_params, width=0.4, label='Original')
    plt.bar(x + 0.2, optimized_params, width=0.4, label='Optimized')
    
    plt.xticks(x, labels)
    plt.ylabel("Values")
    plt.legend()
    plt.title("Optimized Vehicle Suspension Parameters (GA)")
    plt.show()


optimized_params = optimize_vehicle_dynamics_ga()

original_params = [100, 0.5, 50]  # Initial guess
plot_results(original_params, optimized_params)

# Stop MATLAB engine
eng.quit()
