<template>
  <div>
    <h1>Simulation of Reliable Data Transfer</h1>

    <br>

    <p> Run Time: the length of time the protocol will run for </p>
    <p> Sequence Number: the maximum number of the range of sequence numbers that will be used</p>
    <p> Window Size: the maximum number of packets that can be sent at any one time</p>
    <p> Error Rate: the percentage of packets that will pick up bit errors while in transfer</p>
    <p> Loss Rate: the percentage of packets that will be lost before reaching their destination</p>

    <br>

    <p>Rdt2.2: Bit errors but no packet loss, recovery using only ACKs</p>
    <p>Rdt2.1: Bit errors but no packet loss, recovery using both ACKs and NAKs.
      Sender can now detect and recover from corrupted ACKs or NAKs</p>
    <p>Rdt2.0: Bit errors but no packet loss, recovery using both ACKs and NAKs.
      Sender can not recover from corrupted ACKs or NAKs which leads to an inifinite loop</p>
    <p>Rdt1.0: No bit errors or packet loss </p>
  </div>
</template>

<script>

export default {
  name: 'Home',
};
</script>
