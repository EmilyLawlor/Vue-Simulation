<template>
    <div class="options">
        <div>
            Run Time: {{ this.runTimeSlider }}
            <p v-if="this.runTimeSlider == 1">minute</p>
            <p v-else>minutes</p>
            <vue-slider
                v-model="runTimeSlider"
                :min=0.5
                :max=3
                :interval=0.5
                :disabled=isDisabled
            />
        </div>

        <div v-if="showExtraOptions" && false>
            Sequence Numbers: {{ this.sequenceNumbersSlider }}
            <vue-slider
                v-model="sequenceNumbersSlider"
                :min=5
                :max=20
                :disabled=isDisabled
            />
        </div>

        <div v-if="protocol!='Stop-and-Wait' && showExtraOptions">
            Window Size: {{ this.windowSizeSlider }}
            <vue-slider
                v-model="windowSizeSlider"
                :min=1
                :max=20
                :disabled=isDisabled
            />
        </div>

        <div v-if="showErrorRate">
            Error Rate: {{ this.errorRateSlider }}%
            <vue-slider
                v-model="errorRateSlider"
                :min=0
                :max=100
                :interval=10
                :disabled=isDisabled
            />
        </div>

        <div v-if="showExtraOptions">
            Loss Rate: {{ this.lossRateSlider }}%
            <vue-slider
                v-model="lossRateSlider"
                :min=0
                :max=100
                :interval=10
                :disabled=isDisabled
            />
        </div>
    </div>
</template>

<script>
import VueSlider from 'vue-slider-component';
import 'vue-slider-component/theme/antd.css';

export default {
  name: 'Options',
  props: {
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
    isDisabled: Boolean,
    protocol: String,
  },
  components: {
    VueSlider,
  },
  data() {
    return {
      runTimeSlider: this.runTime,
      sequenceNumbersSlider: this.sequenceNumbers,
      windowSizeSlider: this.windowSize,
      errorRateSlider: this.errorRate,
      lossRateSlider: this.lossRate,
    };
  },
  computed: {
    showErrorRate() {
      return this.protocol !== 'rdt1.0';
    },
    showExtraOptions() {
      let show = true;
      if (this.protocol === 'rdt1.0') { show = false; }
      if (this.protocol === 'rdt2.0') { show = false; }
      if (this.protocol === 'rdt2.1') { show = false; }
      if (this.protocol === 'rdt2.2') { show = false; }
      return show;
    },
  },
  watch: {
    runTimeSlider(newVal, oldVal) {
      // this check is mandatory to prevent endless cycle
      if (newVal !== oldVal) this.$emit('update-run-time', newVal);
    },
    sequenceNumbersSlider(newVal, oldVal) {
      // this check is mandatory to prevent endless cycle
      if (newVal !== oldVal) this.$emit('update-sequence-numbers', newVal);
    },
    windowSizeSlider(newVal, oldVal) {
      // this check is mandatory to prevent endless cycle
      if (newVal !== oldVal) this.$emit('update-window-size', newVal);
    },
    errorRateSlider(newVal, oldVal) {
      // this check is mandatory to prevent endless cycle
      if (newVal !== oldVal) this.$emit('update-error-rate', newVal);
    },
    lossRateSlider(newVal, oldVal) {
      // this check is mandatory to prevent endless cycle
      if (newVal !== oldVal) this.$emit('update-loss-rate', newVal);
    },
  },
};
</script>

<style scoped>

.options {
    width: 150px;
    position: absolute;
    right: 0;
    padding: 10px;
    border: 1px solid black;
    border-radius: 10px;
    margin-right: 5px;
}

.options div {
  padding: 5px;
}

</style>
