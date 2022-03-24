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
    };
  },
  methods: {
    updateRunTime(value) {
      this.runTime = value;
    },
    updateErrorRate(value) {
      this.errorRate = value;
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
        console.log(data.generated);
      }, false);
    } catch (err) {
      console.log(err);
    }

    try {
      eventSource.addEventListener('start', (event) => {
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
