class ENVIRONMENT:

        def __init__(self):

		pass

        def Send_To_Simulator(self,simulator,numRobotBodyParts):

                simulator.Send_Box(objectID = numRobotBodyParts , x=0, y=+8, z=0.25, length=0.5, width=0.5, height=0.5, r=1, g=0, b=0)

                simulator.Send_Light_Source( objectIndex = numRobotBodyParts )

                # simulator.Send_Box(objectID = numRobotBodyParts + 1 , x=8, y=0, z=0.25, length=0.5, width=0.5, height=0.5, r=0, g=1, b=0)

                # simulator.Send_Box(objectID = numRobotBodyParts + 2, x=-8, y=0, z=0.25, length=0.5, width=0.5, height=0.5, r=0, g=0, b=1)

                # simulator.Send_Box(objectID = numRobotBodyParts + 3, x=0, y=-8, z=0.25, length=0.5, width=0.5, height=0.5, r=1, g=1, b=1)	
