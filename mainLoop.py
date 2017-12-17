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
    change = stepperArm.getTotalChange(replicaArm)

    if change > 5:
        stepperArm.sendTargetPositions(
                -replicaArm.posDict["X"], 
                replicaArm.posDict["Y"], 
                -replicaArm.posDict["Z"], 
                replicaArm.posDict["A"])
        time.sleep(0.3)
    time.sleep(0.1)

    #stepperArm.sendTargetPositions(0, 0, 0, 9)
    # 1. get the current values for the 4 joints!
    # 2. values = 512 - current values
    # 3. values * 0.01
    # 4. set values as absolut
