<template>
  <v-chip v-bind="$attrs" v-on="$listeners">
    <v-avatar left v-if="count !== null">
      {{ count }}
    </v-avatar>
    <slot />
  </v-chip>
</template>

<script>
export default {
  name: "CounterChip",
  extends: "v-chip",
  props: {
    count: {
      type: [Number, null],
      required: false,
      default: null,
    },
  },
};
</script>
