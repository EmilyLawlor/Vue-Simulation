<template>
  <div>
    <StartButton
      endpoint='/stop-and-wait'
      :updates="this.updates"
      :protocol="this.protocol"
      :isDisabled="isRunning"

      :runTime="this.runTime"
      :sequenceNumbers="this.sequenceNumbers"
      :errorRate="this.errorRate"
      :lossRate="this.lossRate"
      :generation="this.generation"
    />
    <div class="updates">
      <p>{{ updates }}</p>
    </div>
    <canvas id="canvas"/>
    <Legend/>
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
      @update-error-rate="updateErrorRate"
      @update-loss-rate="updateLossRate"
      @update-generation-method="updateGenerationMethod"

      :isDisabled="isRunning"

      :protocol="this.protocol"
    />
  </div>
</template>

<script>
import Options from '@/components/Options.vue';
import StartButton from '@/components/StartButton.vue';
import Statistics from '@/components/Statistics.vue';
import Legend from '@/components/Legend.vue';
import { setUpEventListeners } from '@/utils/eventListeners';
import { generatePackets, usable, resetCanvas } from '@/utils/packetManager';

export default {
  name: 'StopAndWait',
  components: {
    StartButton,
    Options,
    Statistics,
    Legend,
  },
  data() {
    return {
      updates: '',
      isRunning: false,

      runTime: 1,
      sequenceNumbers: 20,
      errorRate: 10,
      lossRate: 10,

      protocol: 'Stop-and-Wait',

      sent: 0,
      generated: 0,
      lost: 0,
      errors: 0,

      sender: [],
      receiver: [],

      generation: 'Normal',
    };
  },
  methods: {
    updateRunTime(value) {
      this.runTime = value;
    },
    updateSequenceNumbers(value) {
      this.sequenceNumbers = value;
    },
    updateErrorRate(value) {
      this.errorRate = value;
    },
    updateLossRate(value) {
      this.lossRate = value;
    },
    updateGenerationMethod(value) {
      this.generation = value;
    },
    generatePackets() {
      [this.sender, this.receiver] = generatePackets(1);
    },
    slideWindow(packet) {
      if (packet < this.sender.length) {
        usable(this.sender[packet]);
        usable(this.receiver[packet]);
      }
    },
  },
  mounted() {
    resetCanvas();
    const eventSource = new EventSource('http://localhost:5000/stream');
    this.generatePackets();
    setUpEventListeners(eventSource, false, this.sender, this.receiver);

    try {
      eventSource.addEventListener('publish', (event) => {
        if (this.isRunning) {
          const data = JSON.parse(event.data);
          this.updates = ` ${data.message}\n ${this.updates}`;
        }
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('terminate', (event) => {
        if (this.isRunning) {
          const data = JSON.parse(event.data);
          this.updates = ` ${data.message}\n ${this.updates}`;
          this.isRunning = false;
          this.generated = data.generated;
          this.sent = data.successfullySent;
          this.lost = data.lost;
          this.errors = data.errors;
        }
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('start', (event) => {
        this.generatePackets();
        const data = JSON.parse(event.data);
        if (data.protocol === this.protocol) {
          this.updates = '';
          this.isRunning = true;
        }
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('ACKreceived', (event) => {
        const data = JSON.parse(event.data);
        this.slideWindow(data.seqnum + 1);
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
