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
import Legend from '@/components/Legend.vue';
import { setUpEventListeners } from '@/utils/eventListeners';
import { generatePackets } from '@/utils/packetManager';

export default {
  name: 'Others',
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
      [this.sender, this.receiver] = generatePackets(1);
    },
  },
  watch: {
    $route() {
      this.generatePackets();
      this.updates = '';
    },
  },
  mounted() {
    const eventSource = new EventSource('http://localhost:5000/stream');
    this.generatePackets();
    setUpEventListeners(eventSource, true, this.sender, this.receiver);

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
        if (data.protocol === this.$route.params.protocol) {
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
