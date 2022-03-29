<template>
  <div>
      <StartButton
        endpoint="/others"
        :updates="this.updates"
        :protocol="this.$route.params.protocol"
        :isDisabled="isRunning"

        :runTime="this.runTime"
        :errorRate="this.errorRate"

      />
    <div class="updates">
      <p>{{ updates }}</p>
    </div>
    <canvas id="canvas"/>
    <Statistics
      class="stats"
      :generated="this.generated"
      :sent="this.sent"
      :lost="this.lost"
      :errors="this.errors"
    />
    <Options
      @update-run-time="updateRunTime"
      @update-error-rate="updateErrorRate"

      :isDisabled="isRunning"

      :protocol="this.$route.params.protocol"
    />
  </div>
</template>

<script>
import Options from '@/components/Options.vue';
import StartButton from '@/components/StartButton.vue';
import Statistics from '@/components/Statistics.vue';
import {
  generatePackets, sendPacket,
  sendACK, sendNAK, resend, error,
} from '@/views/packetManager';

export default {
  name: 'Others',
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
      errorRate: 10,

      sent: 0,
      generated: 0,
      lost: 0,
      errors: 0,

      sender: [],
      receiver: [],
    };
  },
  methods: {
    updateRunTime(value) {
      this.runTime = value;
    },
    updateErrorRate(value) {
      this.errorRate = value;
    },
    generatePackets() {
      [this.sender, this.receiver] = generatePackets();
    },
  },
  mounted() {
    const eventSource = new EventSource('http://localhost:5000/stream');
    this.generatePackets();

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
        this.generatePackets();
        const data = JSON.parse(event.data);
        if (data.protocol === this.$route.params.protocol) {
          this.updates = '';
          this.isRunning = true;
        }
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('send', (event) => {
        const data = JSON.parse(event.data);
        if (data.packetNumber <= this.sender.length) {
          this.sender[data.packetNumber] = sendPacket(data.packetNumber);
        }
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('ACK', (event) => {
        const data = JSON.parse(event.data);
        if (data.packetNumber >= 0 && data.packetNumber <= this.receiver.length) {
          this.receiver[data.packetNumber] = sendACK(data.packetNumber);
        }
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('NAK', (event) => {
        const data = JSON.parse(event.data);
        if (data.packetNumber <= this.receiver.length) {
          this.receiver[data.packetNumber] = sendNAK(data.packetNumber);
        }
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('error', (event) => {
        const data = JSON.parse(event.data);
        if (data.packetNumber <= this.receiver.length) {
          if (data.source === 'sender') {
            error(this.sender[data.packetNumber]);
          } else {
            error(this.receiver[data.packetNumber]);
          }
        }
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('resend', (event) => {
        const data = JSON.parse(event.data);
        if (data.packetNumber <= this.receiver.length) {
          this.sender[data.packetNumber] = resend(data.packetNumber);
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
