<template>
  <div>
      <p id='error'> 🔴 - Error </p>
      <p id='acked'> 🟢 - ACKed </p>
      <p id='sending'> 🔵 - Sending/waiting to send </p>
      <p id='lost'> When a packet disappears, it has been lost in the channel </p>
  </div>
</template>

<script>

export default {
  name: 'Legend',
};
</script>

<style scoped>
div {
    position: absolute;
    text-align: left;
    bottom: 0;
    right: 40%;
}

.error {
    color: red;
}
</style>
