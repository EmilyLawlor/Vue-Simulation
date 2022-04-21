<template>
  <div>
      <StartButton
        endpoint="/go-back-n"
        :updates="this.updates"
        :protocol="this.protocol"
        :isDisabled="isRunning"

        :runTime="this.runTime"
        :sequenceNumbers="this.sequenceNumbers"
        :windowSize="this.windowSize"
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
      @update-window-size="updateWindowSize"
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
import {
  generatePackets, usable, unusable,
  ack, resetCanvas,
} from '@/utils/packetManager';

export default {
  name: 'GoBackN',
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
      windowSize: 5,
      errorRate: 10,
      lossRate: 10,

      sent: 0,
      generated: 0,
      lost: 0,
      errors: 0,

      protocol: 'Go-Back-N',

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
    updateWindowSize(value) {
      this.windowSize = value;
      for (let i = 0; i < this.windowSize; i += 1) {
        usable(this.sender[i]);
        usable(this.receiver[i]);
      }
      for (let i = this.windowSize; i < 20; i += 1) {
        unusable(this.sender[i]);
        unusable(this.receiver[i]);
      }
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
      [this.sender, this.receiver] = generatePackets(this.windowSize);
    },
    slideWindow(nextSeqNum, base) {
      for (let i = nextSeqNum; i < base; i += 1) {
        if (i < this.sender.length) {
          console.log(this.sender[i].state)
          if (this.sender[i].state === 'unusable') {
            usable(this.sender[i]);
            usable(this.receiver[i]);
          }
        }
      }
    },
    // when an ACK is received, ACK all unACked packets before it
    ack(packet) {
      for (let i = 0; i < packet; i += 1) {
        ack(this.sender[i]);
        ack(this.receiver[i]);
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
        const data = JSON.parse(event.data);
        if (data.protocol === this.protocol) {
          this.generatePackets();
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
        this.slideWindow(data.seqnum, data.base + this.windowSize - 1);
        this.ack(data.seqnum);
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
