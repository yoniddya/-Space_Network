from space_network_lib import *
import time

class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):
        super().__init__(packet_to_relay, sender, proxy)


    def __repr__(self):
        return f"RelayPacket(Relaying [{self.data}] via {self.receiver} from {self.sender})"


class BrokenConnectionError(Exception):
    pass


class Satellite(SpaceEntity):
    def __init__(self, name, earth_from_distance):
        super().__init__(name, earth_from_distance)

    def receive_signal(self, packet: Packet):
        if isinstance(packet, RelayPacket):
            inner_packet = packet.data
            print(f"Unwrapping and forwarding to {inner_packet.receiver}")
            try:
                attempt_transmission(inner_packet)
            except BrokenConnectionError:
                print("failed Transmission")
        else:
            print(f"Final destination reached: {packet.data}")
            print(f"[{self.name}] Received: {packet}")

class Earth(SpaceEntity):
    def __init__(self , name, earth_from_distance ):
        super().__init__(name, earth_from_distance)

    def receive_signal(self, packet: Packet):
        pass


network = SpaceNetwork(level=4)
Sat1 = Satellite("Sat1", 100)
Sat2 = Satellite("Sat2", 200)
Sat3 = Satellite("Sat3",300)
Sat4 = Satellite("Sat4",400)
earth = Earth("earth" ,0)


message = Packet("hello from earth", Sat3, Sat4)
p_sat2_to_sat_3 = RelayPacket(message,Sat2, Sat3)
p_sat1_to_sat2 = RelayPacket(p_sat2_to_sat_3,Sat1, Sat2)
p_earth_set1 = RelayPacket(p_sat1_to_sat2, earth, Sat1)



def attempt_transmission(packet: Packet):
    while True:
        try:
            network.send(packet)
            break
        except TemporalInterferenceError:
            print("Interference, waiting...")
            time.sleep(2)
        except DataCorruptedError:
            print("Data corrupted, retrying...")
        except (LinkTerminatedError, OutOfRangeError)as e:
            print("Transmission failed permanently", e)
            raise BrokenConnectionError("BrokenConnectionError")


# attempt_transmission(message)
try:
    attempt_transmission(p_earth_set1)
except BrokenConnectionError:
    print( "failed Transmission")



