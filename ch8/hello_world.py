import qiskit


class IBMQ_JobManager:

    def __init__(self):
      	self.data = []
        
    def createProgram(self,quantum,classical):
        qr = qiskit.QuantumRegister(quantum)
        cr = qiskit.ClassicalRegister(classical)
        program = qiskit.QuantumCircuit(qr, cr)
        return qr,cr,program
    
    def measure(self,program,qr,cr):
        program.measure(qr,cr)
            
    def getIBMQBackend(self):
        qiskit.IBMQ.load_accounts()
        backend = qiskit.providers.ibmq.least_busy(qiskit.IBMQ.backends(simulator=False))
        return backend
    
    def executeProgramOnIBMQ(self,program,backend):
        job = qiskit.execute( program, backend  )
        return job
        

jobManager = IBMQ_JobManager()

quantumRegister,classicalRegister,program = jobManager.createProgram(1,1)

jobManager.measure(program,quantumRegister,classicalRegister)


backend = jobManager.getIBMQBackend()


print("We'll use the least busy device:",backend.name())


job = jobManager.executeProgramOnIBMQ(program,backend)

print( job.result().get_counts() )








