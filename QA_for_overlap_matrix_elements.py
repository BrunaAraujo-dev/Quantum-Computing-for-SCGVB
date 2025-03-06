#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:57:45 2024

@author: bdemoraesaraujo@chem.polimi.it
"""

# Import necessary Qiskit modules
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np
import os


# Function to read Pauli strings and their coefficients from a file
def read_pauli_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    pauli_strings = []
    for line in lines:
        line = line.strip()  # Remove extra spaces/newlines
        if line:
            coefficient, pauli_str = line.split(' * ')
            pauli_strings.append((complex(coefficient), pauli_str))  # Store as (coefficient, Pauli string)
    return pauli_strings

# Function to load all Pauli strings from the given list of file paths
def load_pauli_strings(f_files, w_files):
    f_pauli_strings = [read_pauli_file(f_file) for f_file in f_files]  # Get all Pauli strings from each file
    w_pauli_strings = [read_pauli_file(w_file) for w_file in w_files]  # Get all Pauli strings from each file
    return f_pauli_strings, w_pauli_strings

# Function to apply Pauli operators based on a Pauli string to a quantum circuit
def apply_pauli_string(qc, pauli_str, qubits):
    for i, pauli in enumerate(pauli_str):
        if pauli == 'X':
            qc.x(qubits[i])
        elif pauli == 'Y':
            qc.y(qubits[i])
        elif pauli == 'Z':
            qc.z(qubits[i])
        # 'I' is identity, so no gate is applied

# Function to construct the circuit for computing ⟨ψ_I | ψ_J⟩ for a single pair of Pauli strings
def construct_overlap_circuit(f_pauli_str, w_pauli_str, n_qubits):
    qc = QuantumCircuit(n_qubits)

    # Apply the Pauli string f_J to the initial state |φ_0⟩ = |00000000⟩
    apply_pauli_string(qc, f_pauli_str, range(n_qubits))
   
    # Apply w_I† (adjoint of w_I, which is just the same Pauli string since Pauli operators are Hermitian)
    apply_pauli_string(qc, w_pauli_str, range(n_qubits))

    # The resulting state will be |ψ_I⟩ = w_I† f_J |φ_0⟩
    qc.measure_all()  # Measure all qubits
   
    return qc

# Function to calculate the full overlap matrix O_{IJ}
def calculate_overlap_matrix(f_pauli_strings_list, w_pauli_strings_list, n_qubits):
    simulator = AerSimulator()

    # Initialize an empty matrix to store the results
    overlap_matrix = np.zeros((len(f_pauli_strings_list), len(w_pauli_strings_list)), dtype=complex)
    normalization_factor = 16  # Normalization factor
   
    # Iterate over w_files and f_files
    for i, w_pauli_strings in enumerate(w_pauli_strings_list):
        for j, f_pauli_strings in enumerate(f_pauli_strings_list):
            total_overlap = 0  # Initialize scalar value for the overlap of the (i,j) matrix element

            # For each combination of Pauli strings in f and w
            for f_pauli_tuple in f_pauli_strings:
                for w_pauli_tuple in w_pauli_strings:
                    f_coefficient, f_pauli_str = f_pauli_tuple
                    w_coefficient, w_pauli_str = w_pauli_tuple

                    # Construct the circuit for ⟨ψ_I | ψ_J⟩
                    qc = construct_overlap_circuit(f_pauli_str, w_pauli_str, n_qubits)
                   
                    # Transpile and run the circuit on the simulator
                    transpiled_qc = transpile(qc, simulator)
                    result = simulator.run(transpiled_qc, shots=1024).result()
                    counts = result.get_counts()

                    # Calculate the probability of measuring the |000...000⟩ state
                    zero_state = '0' * n_qubits
                    prob_zero_state = counts.get(zero_state, 0) / 1024  # Normalizing by number of shots
                   
                    # Overlap contribution
                    overlap_contribution = f_coefficient * w_coefficient * prob_zero_state
                    total_overlap += overlap_contribution  # Accumulate overlap

            # Apply normalization factor
            overlap_matrix[i, j] = total_overlap * normalization_factor

    # Enforce specific conditions for antisymmetry
    custom_conditions = [
        (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
        (3, 2), (2, 4), (5, 2), (6, 2),
        (3, 4), (5, 3), (6, 3),
        (4, 5), (4, 6), (6, 5)
    ]

    for i, j in custom_conditions:
        # Convert to zero-based indexing
        i, j = i - 1, j - 1
        overlap_matrix[j, i] = -overlap_matrix[i, j]

    return overlap_matrix

# List of file names for w and f operators
w_files = [
    'pauli_product_output_w1.txt',
    'pauli_product_output_w2.txt',
    'pauli_product_output_w3.txt',
    'pauli_product_output_w4.txt',
    'pauli_product_output_w5.txt',
    'pauli_product_output_w6.txt'
]

f_files = [
    'pauli_product_output_f1.txt',
    'pauli_product_output_f2.txt',
    'pauli_product_output_f3.txt',
    'pauli_product_output_f4.txt',
    'pauli_product_output_f5.txt',
    'pauli_product_output_f6.txt'
]

n_qubits = 8  # The number of qubits (since we're working with an 8-qubit initial state |00000000⟩)

# Load the Pauli strings from the files
f_pauli_strings_list, w_pauli_strings_list = load_pauli_strings(f_files, w_files)

# Calculate the overlap matrix
overlap_matrix = calculate_overlap_matrix(f_pauli_strings_list, w_pauli_strings_list, n_qubits)

# Print the full overlap matrix
print("\nOverlap matrix O_{IJ} after normalization by 16:")
print(overlap_matrix)

# Define the path to save the matrix as a text file
base_path = "/home/bdemoraesaraujo"
output_file_path_txt = os.path.join(base_path, "matrix_elements_real_output_with_conditions.txt")

# Save the matrix to a text file with tab-separated values
np.savetxt(output_file_path_txt, overlap_matrix.real, fmt='%.10f', delimiter='\t')

print(f"Normalized matrix elements real part saved to {output_file_path_txt}")
