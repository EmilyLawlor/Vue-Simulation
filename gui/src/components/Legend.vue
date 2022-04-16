<template>
  <div>
      <p> 🟠 - Sent but not yet ACKed</p>
      <p> 🟢 - Sent and ACKed </p>
      <p> 🔴 - Error </p>
      <p> 🔵 - Usable(within window) but not yet sent</p>
      <p> ⚫ - Unusable, outside of window </p>
      <p> When a packet disappears, it has been lost in the channel </p>
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
</style>
