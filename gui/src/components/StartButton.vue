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
  computed: {
    params() {
      if (this.protocol === 'rdt1.0') {
        return { runTime: this.runTime, protocol: this.protocol };
      }
      if (this.protocol === 'Stop and Wait' || this.protocol === 'Go Back N' || this.protocol === 'Selective Repeat') {
        return {
          runTime: this.runTime,
          sequenceNumbers: this.sequenceNumbers,
          windowSize: this.windowSize,
          errorRate: this.errorRate,
          lossRate: this.lossRate,
        };
      }
      return { runTime: this.runTime, errorRate: this.errorRate, protocol: this.protocol };
    },
  },
  methods: {
    start() {
      const path = `http://localhost:5000${this.endpoint}`;
      axios.get(path, {
        params: this.params,
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
