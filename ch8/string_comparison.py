
import sys
import numpy as np
import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute
from qiskit import IBMQ, BasicAer





YEAST     = "----------------------------------MM----------------------------"
PROTOZOAN = "--MM---------------M------------MMMM---------------M------------"
BACTERIAL = "---M---------------M------------MMMM---------------M------------"

class QASM_Job:

    def __init__(self):
      	self.data = []
        
    def createQuantumRegister(self,quantum,name):
        qr = qiskit.QuantumRegister(quantum,name)
        return qr
    def createClassicalRegister(self,classic,name):
        cr = qiskit.ClassicalRegister(classic,name)
        return cr
    def getQuantumCircuit(self,quantumRegister,classicRegister):
        circ = qiskit.QuantumCircuit(quantumRegister,classicRegister)
        return circ
        
    def getMeasure(self,qr,cr):
        measure = qiskit.QuantumCircuit(qr, cr)
        return measure
        
            
    def getQASMBackend(self):
        backend = qiskit.BasicAer.get_backend('qasm_simulator')
        return backend
    
    def executeCircuitOnQASM(self,program,backend):
        job = qiskit.execute( program, backend)
        return job



def encode_bitstring(bitstring, qr, cr, inverse=False):
    n = math.ceil(math.log2(len(bitstring))) + 1                 
    
    assert n > 2, "the length of bitstring must be at least 2"
    
    qc = QuantumCircuit(qr, cr)
    
      desired_vector = np.array([ 0.0 for i in range(2**n) ])     
      amplitude = np.sqrt(1.0/2**(n-1))
    
    for i, b in enumerate(bitstring):
        pos = i * 2
        if b == "1" or b == "M":
            pos += 1
        desired_vector[pos] = amplitude
    if not inverse:
        qc.initialize(desired_vector, [ qr[i] for i in range(n) ] )
        qc.barrier(qr)
    else:
        qc.initialize(desired_vector, [ qr[i] for i in range(n) ] ).inverse()  #invert the circuit
        for i in range(n):
            qc.measure(qr[i], cr[i])
    print()
    return qc




n = math.ceil(math.log2(len(YEAST))) + 1                 

job = QASM_Job()
qr = job.createQuantumRegister(2,'q')
cr = job.createClassicalRegister(2,'c')

qc_yeast     = encode_bitstring(YEAST, qr, cr)
qc_protozoan = encode_bitstring(PROTOZOAN, qr, cr)
qc_bacterial = encode_bitstring(BACTERIAL, qr, cr)

circs = {"YEAST": qc_yeast, "PROTOZOAN": qc_protozoan, "BACTERIAL": qc_bacterial}


inverse_qc_yeast     = encode_bitstring(YEAST,     qr, cr, inverse=True)
inverse_qc_protozoan = encode_bitstring(PROTOZOAN, qr, cr, inverse=True)
inverse_qc_bacterial = encode_bitstring(BACTERIAL, qr, cr, inverse=True)

inverse_circs = {"YEAST": inverse_qc_yeast, "PROTOZOAN": inverse_qc_protozoan, "BACTERIAL": inverse_qc_bacterial}







key = "PROTOZOAN"       

backend = backend = job.getQASMBackend()
shots = 1000

combined_circs = {}
count = {}

most_similar, most_similar_score = "", -1.0

for other_key in inverse_circs:
    if other_key == key:
        continue
        
    combined_circs[other_key] = circs[key] + inverse_circs[other_key]  
    job = execute(combined_circs[other_key], backend=backend,shots=shots)
    st = job.result().get_counts(combined_circs[other_key])
    if "0"*n in st:
        sim_score = st["0"*n]/shots
    else:
        sim_score = 0.0
    
    print("Similarity score of",key,"and",other_key,"is",sim_score)
    if most_similar_score < sim_score:
        most_similar, most_similar_score = other_key, sim_score

print("[ANSWER]", key,"is most similar to", most_similar)

