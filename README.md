# Quantum-Computing-for-SCGVB
Here are some codes based on Python using PySCF and Qiskit libraries. 
Here, we are working with non-orthogonal orbitals. The final goal is to evaluate the matrix elements on a quantum simulator and quantum hardware through a proper non-variational hybrid algorithm.

So, the main tasks performed were: 

1. Considering tasks performed in a classical computer.

a) Build the NO orbitals using PySCF (save the output file);
b) Compute the integrals for one and two-body based on these NO orbitals built in the previous step (save the output file);
c) Build the dual ab initio Hamiltonian  with the transformed integrals and orthogonal orbitals (save the output file);
c) Compute the Jordan-Wigner transformation for the NO orbitals computed in item (a) (save the output file). This will be used when we are considering the bra vector of each determinant used to compute the matrix elements;
d) Compute the Jordan-Wigner transformation for the dual Hamiltonian built-in item (c) - which consists of a normal JW mapping (save the output file);


2. Now, tasks are performed in a quantum simulator and quantum hardware. Here, the main point is devising a non-variational quantum algorithm that we can run in the quantum simulator and quantum hardware.
   Initially, we tried to use the format of the QA used in Whaley's paper about this topic. However, as they used another kind of ansatz that model complicated too much and was not suitable for our problem.
   So, to try to reduce the complexity we adopted a straightforward approach.

   e)Compute the overlap matrix elements in a quantum simulator using all the files generated as output of the previous steps;
   f)Compute the Hamiltonian matrix elements in a quantum simulator.

