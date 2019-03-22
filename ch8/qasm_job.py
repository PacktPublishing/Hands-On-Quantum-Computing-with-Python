import qiskit

class QASM_Job:

    def __init__(self):
      	self.data = []
        
    def createRegister(self,quantum,name):
        qr = qiskit.QuantumRegister(quantum,name)
        return qr
    def getCircuit(self,quantumRegister):
        circ = qiskit.QuantumCircuit(quantumRegister)
        return circ
    
    def measure(self,program,qr,cr):
        program.measure(qr,cr)
            
    def getQASMBackend(self):
        backend = qiskit.BasicAer.get_backend('qasm_simulator')
        return backend
    
    def executeProgramOnQASM(self,program,backend):
        job = qiskit.execute( program, backend  )
        return job

job = QASM_Job()
quantumRegister = job.createRegister(3,'q')
circuit = job.getCircuit(quantumRegister)

circuit.h(quantumRegister[0])
circuit.cx(quantumRegister[0], quantumRegister[1])
circuit.cx(quantumRegister[0], quantumRegister[2])

circuit.draw()

backend = job.getQASMBackend()

job = qiskit.execute(circuit, backend)


result = job.result()


print("result",result)


