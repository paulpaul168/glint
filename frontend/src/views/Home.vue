<template>
  <FileView />
</template>

<script lang="ts">
import Vue from "vue";
import FileView from "../components/FileView.vue";

export default Vue.extend({
  name: "Home",

  components: {
    FileView,
  },
});
</script>
