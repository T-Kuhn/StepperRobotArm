import time
from stepperRobotArm import StepperRobotArm 
from replicaRobotArm import ReplicaRobotArm 

# - - - - - - - - - - - - - - - - 
# - - -  Global Objects - - - - -
# - - - - - - - - - - - - - - - -
stepperArm = StepperRobotArm()
replicaArm = ReplicaRobotArm()

# - - - - - - - - - - - - - - - - 
# - - - - - MAIN LOOP - - - - - -
# - - - - - - - - - - - - - - - -
while True:
    replicaArm.update()
    # we only want to send the positions if the total change from the currentPosition

    #change = stepperArm.getTotalChange(replicaArm.posDict)

    # here we need to check whether or not the grbl controller is idle or not.
    if stepperArm.checkIfIdle():
        stepperArm.moveToPosition(replicaArm.posDict)
    time.sleep(0.2)
