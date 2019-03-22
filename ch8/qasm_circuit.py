import numpy as np
import qiskit


class QASM_Job:

    def __init__(self):
      	self.data = []
        
    def createQuantumRegister(self,quantum,name):
        qr = qiskit.QuantumRegister(quantum,name)
        return qr
    def createClassicalRegister(self,classic,name):
        cr = qiskit.ClassicalRegister(classic,name)
        return cr
    def getQuantumCircuit(self,quantumRegister):
        circ = qiskit.QuantumCircuit(quantumRegister)
        return circ
        
    def getMeasure(self,qr,cr):
        measure = qiskit.QuantumCircuit(qr, cr)
        return measure
        
            
    def getQASMBackend(self):
        backend = qiskit.BasicAer.get_backend('qasm_simulator')
        return backend
    
    def executeCircuitOnQASM(self,program,backend):
        job = qiskit.execute( program, backend,shots=1024  )
        return job

job = QASM_Job()
quantumRegister = job.createQuantumRegister(3,'q')
classicRegister = job.createClassicalRegister(3,'c')
circuit = job.getQuantumCircuit(quantumRegister)

measure = job.getMeasure(quantumRegister,classicRegister)
measure.barrier(quantumRegister)
measure.measure(quantumRegister,classicRegister)

qc = circuit + measure
qc.draw()

backend_sim = job.getQASMBackend()

job_sim = job.executeCircuitOnQASM(qc,backend_sim)

result_sim = job_sim.result()


counts = result_sim.get_counts(qc)
print(counts)



