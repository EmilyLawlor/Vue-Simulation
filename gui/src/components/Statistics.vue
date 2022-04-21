<template>
  <div>
    <b-table striped hover :items="stats"></b-table>
  </div>
</template>

<script>

export default {
  name: 'Statistics',
  computed: {
    stats() {
      return [
        { Statistics: 'Packets Generated', Value: this.generated },
        { Statistics: 'Packets Successfully Sent', Value: this.sent },
        { Statistics: 'Packets/ACKs Lost', Value: this.lost },
        { Statistics: 'Bit Errors Occurred in Packets/ACKs', Value: this.errors },
      ];
    },
  },
  props: {
    generated: {
      type: Number,
      default: 0,
    },
    sent: {
      type: Number,
      default: 0,
    },
    lost: {
      type: Number,
      default: 0,
    },
    errors: {
      type: Number,
      default: 0,
    },
  },

};
</script>

<style scoped>
div {
  position: absolute;
  bottom: 0;
  right: 0;
}
</style>
