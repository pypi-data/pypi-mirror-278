<template>
  <v-btn color="secondary" v-bind="$attrs">
    <v-icon left>$prev</v-icon>
    {{ $t("actions.back") }}
  </v-btn>
</template>

<script>
export default {
  name: "BackButton",
};
</script>
