import hashlib
import sys

from charm.core.engine.protocol import Protocol
from charm.toolbox.ecgroup import ECGroup,G
from socket import socket, AF_INET, SOCK_STREAM
from charm.toolbox.enum import Enum
from charm.core.math.integer import integer  # pylint: disable=no-name-in-module
from charm.toolbox.integergroup import IntegerGroupQ

party = Enum('Sender', 'Receiver')
SENDER, RECEIVER = party.Sender, party.Receiver
HOST, PORT = "", 8803
SECURITY_PARAM = 5


def get_hash(number):
  return hashlib.sha256(int(number).to_bytes(256, byteorder='big')).digest()

def xor(otp: bytes, msg: bytes) -> bytes:
  return bytes(hash_byte ^ msg_byte for hash_byte, msg_byte in zip(otp, msg))


class OneOfTwo(Protocol):

  def __init__(self):
    super().__init__(None)

    sender_states = {
        1: self.sender_state_1,
        3: self.sender_state_3,
        5: self.sender_state_5,
    }

    receiver_states = {
        2: self.receiver_state_2,
        4: self.receiver_state_4,
    }

    sender_trans = {1: 3, 3: 5}
    receiver_trans = {2: 4}

    self.group = IntegerGroupQ()
    self.group.paramgen(SECURITY_PARAM)

    Protocol.addPartyType(self, SENDER, sender_states, sender_trans, True)
    Protocol.addPartyType(self, RECEIVER, receiver_states, receiver_trans)



  def sender_state_1(self):
    print('Sender generates random value c and computes C = g ^ c.')

    g = self.group.randomGen()
    c = self.group.random()
    C = g ** c
    super().setState(3)
    super().store(('g', g))
    return {'g': g, 'C': C}

  def receiver_state_2(self, data):
    print('Receiver got C, generates PKs and sends to sender.')
    C, g = data['C'], data['g']
    k = self.group.random()
    super().store(('g', g), ('k', k))
    PK_0 = g ** k
    PK_1 = C / (g ** k)
    super().setState(4)
    return {'PK_0': PK_0, 'PK_1': PK_1}

  def sender_state_3(self, data):
    PK_0, PK_1 = data['PK_0'], data['PK_1']
    print('Sender receives PKs, gets messages and calculates.')
    g = self.db['g']
    r0 = self.group.random()
    r1 = self.group.random()
    m0 = b"message 0"
    m1 = b"message 1"
    super().store(('m0', m0), ('m1', m1),)
    c0 = (g ** r0, xor(get_hash(PK_0 ** r0), m0).hex())
    c1 = (g ** r1, xor(get_hash(PK_1 ** r1), m1).hex())
    super().setState(5)
    return {'c0': c0, 'c1': c1}

  def receiver_state_4(self, data):
    c0 = data['c0']
    k, = super().get(['k'])
    w0 = bytes.fromhex(c0[1])
    H = c0[0] ** k
    decoded_msg = xor(get_hash(H), w0)
    super().setState(None)
    return {'decoded_msg': decoded_msg.hex()}

  def sender_state_5(self, data):
    decoded_msg = bytes.fromhex(data['decoded_msg'])
    m0, m1 = super().get(['m0', 'm1'])
    assert decoded_msg == m0
    super().setState(None)
    return None

if __name__ == "__main__":
  one_of_two = OneOfTwo()

  if sys.argv[1] == "-v":
    print("Operating as verifier...")
    svr = socket(AF_INET, SOCK_STREAM)
    svr.bind((HOST, PORT))
    svr.listen(1)
    svr_sock, addr = svr.accept()
    print("Connected by ", addr)
    _name, _type, _sock = "sender", SENDER, svr_sock
  elif sys.argv[1] == "-p":
    print("Operating as prover...")
    clt = socket(AF_INET, SOCK_STREAM)
    clt.connect((HOST, PORT))
    clt.settimeout(15)
    _name, _type, _sock = "receiver", RECEIVER, clt
  else:
    print("Usage: %s [-v or -p]" % sys.argv[0])
    exit(-1)
  one_of_two.setup({'name':_name, 'type':_type, 'socket':_sock})
  # run as a thread...
  one_of_two.execute(_type)
