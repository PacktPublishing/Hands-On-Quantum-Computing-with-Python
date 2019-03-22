import numpy as np
import qiskit
from qiskit import *
from qiskit.tools.monitor import job_monitor, backend_monitor, backend_overview
from qiskit.providers.ibmq import least_busy



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
        
            
    def getIBMQBackend(self):
        qiskit.IBMQ.load_accounts()
        backend = least_busy(IBMQ.backends(filters=lambda x: not x.configuration().simulator))
        return backend
    
    def executeCircuitOnQASM(self,program,backend):
        job = qiskit.execute( program, backend)
        return job

job = QASM_Job()
quantumRegister = job.createQuantumRegister(2,'q')
classicRegister = job.createClassicalRegister(2,'c')
circuit = job.getQuantumCircuit(quantumRegister,classicRegister)
circuit.h(quantumRegister[0])
circuit.cx(quantumRegister[0], quantumRegister[1])
circuit.measure(quantumRegister, classicRegister);


backend = job.getIBMQBackend()

backend.name()

job1 = job.executeCircuitOnQASM(circuit,backend)


job_monitor(job1)



job2 = execute(circuit, backend)
job_monitor(job2, interval=5)



backend_monitor(backend)


backend_overview()







