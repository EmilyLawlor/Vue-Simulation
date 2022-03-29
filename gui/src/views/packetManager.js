import Packet from '@/classes/packets';

// eslint-disable-next-line import/prefer-default-export
export function generatePackets() {
  const sender = [];
  for (let x = 4; x < 300; x += 15) {
    sender.push(new Packet(x, 10));
  }

  const receiver = [];
  for (let x = 4; x < 300; x += 15) {
    receiver.push(new Packet(x, 130));
  }
  return [sender, receiver];
}

// eslint-disable-next-line import/prefer-default-export
export function sendPacket(packetNumber) {
  const x = (packetNumber) * 15 + 4;
  const packet = new Packet(x, 10);
  requestAnimationFrame(() => {
    packet.moveDown(130);
  });
  return packet;
}

// eslint-disable-next-line import/prefer-default-export
export function sendACK(packetNumber) {
  const x = (packetNumber) * 15 + 4;
  const packet = new Packet(x, 130);
  packet.setState('ACKed');
  requestAnimationFrame(() => {
    packet.moveUp(10);
  });
  return packet;
}

// eslint-disable-next-line import/prefer-default-export
export function sendNAK(packetNumber) {
  const x = (packetNumber) * 15 + 4;
  const packet = new Packet(x, 130);
  packet.setState('error');
  requestAnimationFrame(() => {
    packet.moveUp(10);
  });
  return packet;
}

// eslint-disable-next-line import/prefer-default-export
export function resend(packetNumber) {
  // calculate x coordiate of packet
  const x = (packetNumber) * 15 + 4;
  const packet = new Packet(x, 10);
  requestAnimationFrame(() => {
    packet.moveDown(130);
  });
  return packet;
}

// eslint-disable-next-line import/prefer-default-export
export function error(packet) {
  packet.setState('error');
}
