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
    <Options
      @update-run-time="updateRunTime"
      @update-error-rate="updateErrorRate"

      :errorRate="errorRate"
      :isDisabled="isRunning"

      :protocol="this.$route.params.protocol"
    />
  </div>
</template>

<script>
import Options from '@/components/Options.vue';
import StartButton from '@/components/StartButton.vue';

export default {
  name: 'Others',
  components: {
    StartButton,
    Options,
  },
  data() {
    return {
      updates: '',
      isRunning: false,

      runTime: 1,
      errorRate: 0,
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
@import "index.css"
</style>
