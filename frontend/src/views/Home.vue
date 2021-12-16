<template>
  <div class="d-flex flex-row main-pane">
    <div style="max-width: 400px; min-width: 200px; flew-grow: 3">
      <project-list />
    </div>
    <div style="flex-grow: 7">
      <content-view />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import ContentView from "../components/ContentView.vue";
import ProjectList from "../components/ProjectList.vue";

export default Vue.extend({
  name: "Home",

  components: {
    ContentView,
    ProjectList,
  },
});
</script>

<style>
.main-pane {
  width: 100%;
  margin: auto;
  height: 100%;
  /*height: calc(97vh - 56px);*/
}

.main-content-pane {
  height: 100%;
}
</style>
