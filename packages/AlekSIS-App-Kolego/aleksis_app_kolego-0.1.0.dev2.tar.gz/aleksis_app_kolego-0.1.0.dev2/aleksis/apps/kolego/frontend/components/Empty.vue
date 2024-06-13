<template>
  <div class="d-flex justify-center align-center flex-column text-center">
    <h1 class="text-h2" :v-text="appName"></h1>
  </div>
</template>

<script>
import gqlAppName from "./appName.graphql";

export default {
  name: "Empty",
  data() {
    return {
      appName: null,
    };
  },
  apollo: {
    appName: gqlAppName,
  },
};
</script>

<style scoped></style>
