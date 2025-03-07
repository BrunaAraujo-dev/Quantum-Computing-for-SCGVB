# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 22:45:08 2024

@author: Bruna Gabrielly
"""

import sympy as sp
import numpy as np

# Read the overlap integrals from the file, skipping any non-numerical lines
def read_overlap_integrals(filename):
    overlap_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            # Check if the line contains valid numerical data
            if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
                i, j = int(parts[0]), int(parts[1])
                value = float(parts[2])
                overlap_dict[(i, j)] = value
                overlap_dict[(j, i)] = value  # Ensure symmetry in the matrix
    return overlap_dict

# Build a matrix from the overlap dictionary using symbolic variables
def build_matrix_symbolic(row_indices, col_indices):
    matrix = sp.zeros(4, 4)  # Initialize a 4x4 symbolic matrix
    for row, i in enumerate(row_indices):
        for col, j in enumerate(col_indices):
            symbol = sp.Symbol(f'S_{i}{j}')
            matrix[row, col] = symbol
    return matrix

# Compute symbolic determinants
def compute_symbolic_determinants():
    determinants = {}
    # Define matrices based on row and column indices
    matrices_indices = {
        'S_psi1_psi1': ([1, 3, 6, 8], [1, 3, 6, 8]),
        'S_psi1_psi2': ([1, 3, 6, 8], [1, 4, 6, 7]),
        'S_psi1_psi3': ([1, 3, 6, 8], [2, 3, 5, 8]),
        'S_psi1_psi4': ([1, 3, 6, 8], [2, 4, 5, 7]),
        'S_psi1_psi5': ([1, 3, 6, 8], [1, 2, 7, 8]),
        'S_psi1_psi6': ([1, 3, 6, 8], [3, 4, 5, 6]),
        'S_psi2_psi1': ([1, 4, 6, 7], [1, 3, 6, 8]),
        'S_psi2_psi2': ([1, 4, 6, 7], [1, 4, 6, 7]),
        'S_psi2_psi3': ([1, 4, 6, 7], [2, 3, 5, 8]),
        'S_psi2_psi4': ([1, 4, 6, 7], [2, 4, 5, 7]),
        'S_psi2_psi5': ([1, 4, 6, 7], [1, 2, 7, 8]),
        'S_psi2_psi6': ([1, 4, 6, 7], [3, 4, 5, 6]),
        'S_psi3_psi1': ([2, 3, 5, 8], [1, 3, 6, 8]),
        'S_psi3_psi2': ([2, 3, 5, 8], [1, 4, 6, 7]),
        'S_psi3_psi3': ([2, 3, 5, 8], [2, 3, 5, 8]),
        'S_psi3_psi4': ([2, 3, 5, 8], [2, 4, 5, 7]),
        'S_psi3_psi5': ([2, 3, 5, 8], [1, 2, 7, 8]),
        'S_psi3_psi6': ([2, 3, 5, 8], [3, 4, 5, 6]),
        'S_psi4_psi1': ([2, 4, 5, 7], [1, 3, 6, 8]),
        'S_psi4_psi2': ([2, 4, 5, 7], [1, 4, 6, 7]),
        'S_psi4_psi3': ([2, 4, 5, 7], [2, 3, 5, 8]),
        'S_psi4_psi4': ([2, 4, 5, 7], [2, 4, 5, 7]),
        'S_psi4_psi5': ([2, 4, 5, 7], [1, 2, 7, 8]),
        'S_psi4_psi6': ([2, 4, 5, 7], [3, 4, 5, 6]),
        'S_psi5_psi1': ([1, 2, 7, 8], [1, 3, 6, 8]),
        'S_psi5_psi2': ([1, 2, 7, 8], [1, 4, 6, 7]),
        'S_psi5_psi3': ([1, 2, 7, 8], [2, 3, 5, 8]),
        'S_psi5_psi4': ([1, 2, 7, 8], [2, 4, 5, 7]),
        'S_psi5_psi5': ([1, 2, 7, 8], [1, 2, 7, 8]),
        'S_psi5_psi6': ([1, 2, 7, 8], [3, 4, 5, 6]),
        'S_psi6_psi1': ([3, 4, 5, 6], [1, 3, 6, 8]),
        'S_psi6_psi2': ([3, 4, 5, 6], [1, 4, 6, 7]),
        'S_psi6_psi3': ([3, 4, 5, 6], [2, 3, 5, 8]),
        'S_psi6_psi4': ([3, 4, 5, 6], [2, 4, 5, 7]),
        'S_psi6_psi5': ([3, 4, 5, 6], [1, 2, 7, 8]),
        'S_psi6_psi6': ([3, 4, 5, 6], [3, 4, 5, 6])
    }

    for label, (row_indices, col_indices) in matrices_indices.items():
        matrix = build_matrix_symbolic(row_indices, col_indices)
        determinant = matrix.det()  # Compute the symbolic determinant
        determinants[label] = determinant
    return determinants

# Substitute the symbolic Sij values with numerical ones from the overlap integrals file
def substitute_numerical_values(determinants, overlap_dict):
    numerical_determinants = {}
    for label, determinant in determinants.items():
        # Substitute the symbolic S_ij with their corresponding values
        for (i, j), value in overlap_dict.items():
            determinant = determinant.subs(f'S_{i}{j}', value)
        # Evaluate the determinant numerically
        numerical_determinants[label] = determinant.evalf()
    return numerical_determinants

# Print the numerical determinants
def print_numerical_determinants(numerical_determinants):
    for label, determinant in numerical_determinants.items():
        print(f"Determinant of {label}: {determinant}\n")

# Main execution
filename = 'C:/Users/Bruna Gabrielly/Downloads/h4_overlap_integrals.txt'
overlap_dict = read_overlap_integrals(filename)

# Step 1: Compute symbolic determinants
symbolic_determinants = compute_symbolic_determinants()

# Step 2: Substitute with numerical values
numerical_determinants = substitute_numerical_values(symbolic_determinants, overlap_dict)

# Step 3: Print the results
print_numerical_determinants(numerical_determinants)
