<template>
    <button
        type="button"
        class="btn btn-warning btn-sm"
        @click="start()"
        :disabled=isDisabled>
        Start {{ protocol }}
    </button>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StartButton',
  props: {
    endpoint: String,
    updates: String,
    protocol: String,
    isDisabled: Boolean,
    runTime: {
      type: Number,
      default: 1,
    },
    sequenceNumbers: {
      type: Number,
      default: 20,
    },
    windowSize: {
      type: Number,
      default: 5,
    },
    errorRate: {
      type: Number,
      default: 10,
    },
    lossRate: {
      type: Number,
      default: 10,
    },
  },
  methods: {
    start() {
      const path = `http://localhost:5000${this.endpoint}`;
      axios.get(path, {
        params: {
          runTime: this.runTime,
          sequenceNumbers: this.sequenceNumbers,
          windowSize: this.windowSize,
          errorRate: this.errorRate,
          lossRate: this.lossRate,
        },
      })
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>
