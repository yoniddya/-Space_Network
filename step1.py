from space_network_lib import *
class Satellite(SpaceEntity):
    def __init__(self ,name ,earth_from_distance ):
        super().__init__(name ,earth_from_distance)

    def receive_signal(self, packet : Packet):
            print (f"[{self.name}] Received: {packet}")


network = SpaceNetwork(level= 1)
Sat1 = Satellite("Sat1" ,100 )
Sat2 = Satellite("Sat2" ,200 )
massege = Packet("helo world" ,Sat1  ,Sat2)
network.send(massege)