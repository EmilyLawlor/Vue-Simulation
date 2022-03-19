<template>
  <div>
      <StartButton
        endpoint="/selective-repeat"
        :updates="this.updates"
        :protocol="this.protocol"
        :isDisabled="true"

        :runTime="this.runTime"
        :sequenceNumbers="this.sequenceNumbers"
        :windowSize="this.windowSize"
        :errorRate="this.errorRate"
        :lossRate="this.lossRate"
      />
    <div class="updates">
      <p>{{ updates }}</p>
    </div>
    <Options
      @update-run-time="updateRunTime"
      @update-sequence-numbers="updateSequenceNumbers"
      @update-window-size="updateWindowSize"
      @update-error-rate="updateErrorRate"
      @update-loss-rate="updateLossRate"

      :sequenceNumbersSlider="sequenceNumbers"
      :windowSizeSlider="windowSize"
      :errorRateSlider="errorRate"
      :lossRateSlider="lossRate"
      :isDisabled="isRunning"

      :protocol="this.protocol"
    />
  </div>
</template>

<script>
import Options from '@/components/Options.vue';
import StartButton from '@/components/StartButton.vue';

export default {
  name: 'SelectiveRepeat',
  components: {
    StartButton,
    Options,
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

      protocol: 'Selective Repeat',
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
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('start', (event) => {
        const data = JSON.parse(event.data);
        if (data.protocol === 'Selective-Repeat') {
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
@import "index.css"
</style>
