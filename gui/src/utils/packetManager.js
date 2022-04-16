import Packet from '@/classes/packets';

/* eslint-disable import/prefer-default-export */
export function generatePackets(windowSize) {
  let count = 0;
  const sender = [];
  for (let x = 4; x < 300; x += 15) {
    if (count < windowSize) {
      sender.push(new Packet(x, 10, 'usable'));
    } else {
      sender.push(new Packet(x, 10, 'unusable'));
    }
    count += 1;
  }

  count = 0;
  const receiver = [];
  for (let x = 4; x < 300; x += 15) {
    if (count < windowSize) {
      receiver.push(new Packet(x, 130, 'usable'));
    } else {
      receiver.push(new Packet(x, 130, 'unusable'));
    }
    count += 1;
  }
  return [sender, receiver];
}

export function sendPacket(packetNumber) {
  // calculate x coordiate of packet
  const x = (packetNumber) * 15 + 4;
  const packet = new Packet(x, 10, 'sent');
  requestAnimationFrame(() => {
    packet.moveDown(130);
  });
  return packet;
}

export function sendACK(packetNumber) {
  // calculate x coordiate of packet
  const x = (packetNumber) * 15 + 4;
  const packet = new Packet(x, 130, 'ACKed');
  packet.setState('ACKed');
  requestAnimationFrame(() => {
    packet.moveUp(10);
  });
  return packet;
}

export function sendNAK(packetNumber) {
  // calculate x coordiate of packet
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
  const packet = new Packet(x, 10, 'sent');
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

export function usable(packet) {
  packet.setState('usable');
}

export function unusable(packet) {
  packet.setState('unusable');
}

export function ack(packet) {
  packet.setState('ACKed');
}

export function sent(packet) {
  packet.setState('sent');
}

export function resetCanvas() {
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}
/* eslint-disable import/prefer-default-export */
