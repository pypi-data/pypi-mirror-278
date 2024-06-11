<script>
import DateField from "./forms/DateField.vue";
import { DateTime } from "luxon";

export default {
  name: "DateSelectFooter",
  components: {
    DateField,
  },
  props: {
    value: {
      type: String,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  emits: ["input", "prev", "next"],
};
</script>

<template>
  <v-footer app inset padless class="date-select-footer">
    <v-card tile class="full-width">
      <v-card-title class="auto-margin">
        <div class="d-flex align-center justify-center full-width">
          <v-btn icon large class="me-4" @click="$emit('prev')">
            <v-icon>$prev</v-icon>
          </v-btn>
          <div class="flex-grow-0">
            <date-field
              solo-inverted
              flat
              hide-details
              :value="value"
              @input="$emit('input', $event)"
              :label="$t('date_select.label')"
              :disabled="loading"
              readonly
            />
          </div>
          <v-btn icon large class="ms-4" @click="$emit('next')">
            <v-icon>$next</v-icon>
          </v-btn>
        </div>
      </v-card-title>
    </v-card>
  </v-footer>
</template>

<style scoped>
.auto-margin {
  margin: auto;
}
.date-select-footer {
  z-index: 5;
}
</style>
