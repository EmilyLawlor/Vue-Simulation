import Packet from '@/classes/packets';

/* eslint-disable import/prefer-default-export */
export function generatePackets() {
  const sender = [];
  for (let x = 4; x < 300; x += 15) {
    sender.push(new Packet(x, 10, 'waiting'));
  }

  const receiver = [];
  for (let x = 4; x < 300; x += 15) {
    receiver.push(new Packet(x, 130, 'waiting'));
  }
  return [sender, receiver];
}

export function sendPacket(packetNumber) {
  const x = (packetNumber) * 15 + 4;
  const packet = new Packet(x, 10, 'waiting');
  requestAnimationFrame(() => {
    packet.moveDown(130);
  });
  return packet;
}

export function sendACK(packetNumber) {
  const x = (packetNumber) * 15 + 4;
  const packet = new Packet(x, 130, 'ACKed');
  packet.setState('ACKed');
  requestAnimationFrame(() => {
    packet.moveUp(10);
  });
  return packet;
}

export function sendNAK(packetNumber) {
  const x = (packetNumber) * 15 + 4;
  const packet = new Packet(x, 130, 'error');
  packet.setState('error');
  requestAnimationFrame(() => {
    packet.moveUp(10);
  });
  return packet;
}

export function resend(packetNumber) {
  // calculate x coordiate of packet
  const x = (packetNumber) * 15 + 4;
  const packet = new Packet(x, 10, 'waiting');
  requestAnimationFrame(() => {
    packet.moveDown(130);
  });
  return packet;
}

export function error(packet) {
  packet.setState('error');
}

export function lost(packet) {
  packet.setState('lost');
}
/* eslint-disable import/prefer-default-export */
