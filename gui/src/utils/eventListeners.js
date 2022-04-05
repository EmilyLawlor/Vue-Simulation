/* eslint-disable no-param-reassign */
import {
  sendPacket, lost,
  sendACK, sendNAK, resend, error,
} from '@/utils/packetManager';

// eslint-disable-next-line import/prefer-default-export
export function setUpEventListeners(eventSource, NAK, sender, receiver) {
  try {
    eventSource.addEventListener('send', (event) => {
      const data = JSON.parse(event.data);
      if (data.packetNumber <= sender.length) {
        sender[data.packetNumber] = sendPacket(data.packetNumber);
      }
    }, false);
  } catch (err) {
    console.log(err);
  }

  try {
    eventSource.addEventListener('ACK', (event) => {
      const data = JSON.parse(event.data);
      if (data.packetNumber >= 0 && data.packetNumber <= receiver.length) {
        receiver[data.packetNumber] = sendACK(data.packetNumber);
      }
    }, false);
  } catch (err) {
    console.log(err);
  }

  if (NAK) {
    try {
      eventSource.addEventListener('NAK', (event) => {
        const data = JSON.parse(event.data);
        if (data.packetNumber >= 0 && data.packetNumber <= receiver.length) {
          receiver[data.packetNumber] = sendNAK(data.packetNumber);
        }
      }, false);
    } catch (err) {
      console.log(err);
    }
  }

  try {
    eventSource.addEventListener('resend', (event) => {
      const data = JSON.parse(event.data);
      if (data.packetNumber <= receiver.length) {
        sender[data.packetNumber] = resend(data.packetNumber);
      }
    }, false);
  } catch (err) {
    console.log(err);
  }

  try {
    eventSource.addEventListener('error', (event) => {
      const data = JSON.parse(event.data);
      if (data.source === 'sender' && data.packetNumber <= sender.length) {
        error(sender[data.packetNumber]);
      } if (data.source === 'receiver' && data.packetNumber <= receiver.length) {
        error(receiver[data.packetNumber]);
      }
    }, false);
  } catch (err) {
    console.log(err);
  }

  try {
    eventSource.addEventListener('lost', (event) => {
      const data = JSON.parse(event.data);
      if (data.source === 'sender' && data.packetNumber <= sender.length) {
        lost(sender[data.packetNumber]);
      } if (data.source === 'receiver' && data.packetNumber <= receiver.length) {
        lost(receiver[data.packetNumber]);
      }
    }, false);
  } catch (err) {
    console.log(err);
  }
}
/* eslint-disable no-param-reassign */
