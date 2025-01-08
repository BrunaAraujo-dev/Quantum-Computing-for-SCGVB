# Quantum-Computing-for-SCGVB

This repository contains Python codes utilizing the PySCF and Qiskit libraries. The focus is on working with non-orthogonal orbitals, with the ultimate goal of evaluating matrix elements on quantum simulators and quantum hardware using a non-variational hybrid algorithm.

### Main Tasks

The workflow consists of two major parts:

#### 1. Tasks Performed on a Classical Computer

The following steps are executed using classical computing resources:

a) **Construct Non-Orthogonal (NO) Orbitals**: Use PySCF to build NO orbitals and save the output file.

b) **Compute Integrals**: Calculate one- and two-body integrals based on the NO orbitals generated in the previous step and save the output file.

c) **Build the Dual *Ab Initio* Hamiltonian**: Using the transformed integrals and orthogonal orbitals, construct the dual Hamiltonian and save the output file.

d) **Jordan-Wigner Transformation for NO Orbitals**: Perform the Jordan-Wigner transformation for the NO orbitals computed in step (a) and save the output file. This transformation will be used when considering the bra vector of each determinant for computing the matrix elements.

e) **Jordan-Wigner Transformation for the Dual Hamiltonian**: Perform the Jordan-Wigner transformation on the dual Hamiltonian built in step (c). This step involves a standard JW mapping, and the output file is saved.

#### 2. Tasks Performed on a Quantum Simulator and Quantum Hardware

In this stage, the goal is to implement a non-variational quantum algorithm suitable for quantum simulators and hardware. Initially, we attempted to use the algorithm described in Whaley's paper on this topic. However, their approach, which used a different ansatz, proved overly complex and unsuitable for our problem. To simplify the process, we adopted a more straightforward approach:

f) **Compute Overlap Matrix Elements**: Use a quantum simulator to compute the overlap matrix elements, utilizing the files generated in the previous steps.

g) **Compute Hamiltonian Matrix Elements**: Use a quantum simulator to compute the Hamiltonian matrix elements.

...
