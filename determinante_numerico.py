# -*- coding: utf-8 -*-
import numpy as np

# Read the overlap integrals from the file, skipping any non-numerical lines
def read_overlap_integrals(filename):
    overlap_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            # Check if the line contains valid numerical data
            if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
                i, j, value = int(parts[0]), int(parts[1]), float(parts[2])
                overlap_dict[(i, j)] = value
                overlap_dict[(j, i)] = value  # Ensure symmetry in the matrix
    return overlap_dict

# Build a matrix from the overlap dictionary based on row and column indices
def build_matrix(row_indices, col_indices, overlap_dict):
    matrix = np.zeros((4, 4))
    for row, i in enumerate(row_indices):
        for col, j in enumerate(col_indices):
            matrix[row, col] = overlap_dict.get((i, j), 0)
    return matrix

# Compute the determinants of all matrices
def compute_determinants(overlap_dict):
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
        matrix = build_matrix(row_indices, col_indices, overlap_dict)
        determinant = np.linalg.det(matrix)
        determinants[label] = determinant
    return determinants

# Save the results to a .txt file
def save_determinants_to_file(determinants, filename):
    with open(filename, 'w') as file:
        for label, determinant in determinants.items():
            file.write(f"Determinant of {label}: {determinant}\n")
# Print the results
def print_determinants(determinants):
    for label, determinant in determinants.items():
        print(f"Determinant of {label}: {determinant}")

# Main execution
input_filename = 'C:/Users/Bruna Gabrielly/Downloads/h4_overlap_integrals.txt'
output_filename = 'C:/Users/Bruna Gabrielly/Downloads/determinants_results.txt'

overlap_dict = read_overlap_integrals(input_filename)
determinants = compute_determinants(overlap_dict)
save_determinants_to_file(determinants, output_filename)

print(f"Determinants have been computed and saved to {output_filename}")

print_determinants(determinants)
