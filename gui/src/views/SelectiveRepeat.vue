<template>
  <div>
    <StartButton
      endpoint="/selective-repeat"
      :updates="this.updates"
      :protocol="this.protocol"
      :isDisabled="isRunning"

      :runTime="this.runTime"
      :sequenceNumbers="this.sequenceNumbers"
      :windowSize="this.windowSize"
      :errorRate="this.errorRate"
      :lossRate="this.lossRate"
    />
    <div class="updates">
      <p>{{ updates }}</p>
    </div>
    <Statistics
      class="stats"
      :generated="this.generated"
      :sent="this.sent"
      :lost="this.lost"
      :errors="this.errors"
    />
    <Options
      @update-run-time="updateRunTime"
      @update-sequence-numbers="updateSequenceNumbers"
      @update-window-size="updateWindowSize"
      @update-error-rate="updateErrorRate"
      @update-loss-rate="updateLossRate"

      :isDisabled="isRunning"

      :protocol="this.protocol"
    />
  </div>
</template>

<script>
import Options from '@/components/Options.vue';
import StartButton from '@/components/StartButton.vue';
import Statistics from '@/components/Statistics.vue';

export default {
  name: 'SelectiveRepeat',
  components: {
    StartButton,
    Options,
    Statistics,
  },
  data() {
    return {
      updates: '',
      isRunning: false,

      runTime: 1,
      sequenceNumbers: 20,
      windowSize: 5,
      errorRate: 0,
      lossRate: 0,

      sent: 0,
      generated: 0,
      lost: 0,
      errors: 0,

      protocol: 'Selective-Repeat',
    };
  },
  methods: {
    updateRunTime(value) {
      this.runTime = value;
    },
    updateSequenceNumbers(value) {
      this.sequenceNumbers = value;
    },
    updateWindowSize(value) {
      this.windowSize = value;
    },
    updateErrorRate(value) {
      this.errorRate = value;
    },
    updateLossRate(value) {
      this.lossRate = value;
    },
  },
  mounted() {
    const eventSource = new EventSource('http://localhost:5000/stream');

    try {
      eventSource.addEventListener('publish', (event) => {
        const data = JSON.parse(event.data);
        this.updates += `${data.message}\n`;
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('terminate', (event) => {
        const data = JSON.parse(event.data);
        this.updates += `${data.message}\n`;
        this.isRunning = false;
        this.generated = data.generated;
        this.sent = data.successfullySent;
        this.lost = data.lost;
        this.errors = data.errors;
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('start', (event) => {
        const data = JSON.parse(event.data);
        if (data.protocol === this.protocol) {
          this.updates = '';
          this.isRunning = true;
        }
      }, false);
    } catch (err) {
      console.log(err);
    }
  },
};
</script>

<style scoped>
@import "index.css";
</style>
