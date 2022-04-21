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

        <div v-if="showExtraOptions && false">
            Sequence Numbers: {{ this.sequenceNumbersSlider }}
            <vue-slider
                v-model="sequenceNumbersSlider"
                :min=5
                :max=20
                :disabled=true
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

        <div>
          Packet Generation Method: {{ generation }}
          <select v-model="generation" class="form-select" size="4">
            <option selected value="Normal">Normal Distribution</option>
            <option value="Exponential">Exponential Distribution</option>
            <option value="5">Every 5 Seconds</option>
            <option value="3">Every 3 Seconds</option>
          </select>
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
      generation: 'Normal',
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
    runTimeSlider(newRunTime, oldRunTime) {
      if (newRunTime !== oldRunTime) this.$emit('update-run-time', newRunTime);
    },
    sequenceNumbersSlider(newSequenceNum, oldSequenceNum) {
      if (newSequenceNum !== oldSequenceNum) this.$emit('update-sequence-numbers', newSequenceNum);
    },
    windowSizeSlider(newWindowSize, oldWindowSize) {
      if (newWindowSize !== oldWindowSize) this.$emit('update-window-size', newWindowSize);
    },
    errorRateSlider(newError, oldError) {
      if (newError !== oldError) this.$emit('update-error-rate', newError);
    },
    lossRateSlider(newLoss, oldLoss) {
      if (newLoss !== oldLoss) this.$emit('update-loss-rate', newLoss);
    },
    generation(newMethod, oldMethod) {
      if (newMethod !== oldMethod) this.$emit('update-generation-method', newMethod);
    },
  },
};
</script>

<style scoped>

.options {
    width: 14%;
    min-width: 130px;
    max-width: 200px;
    position: absolute;
    top: 15%;
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
