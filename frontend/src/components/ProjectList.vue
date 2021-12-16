<template>
  <div class="d-flex flex-column main-content-pane projects-panel">
    <v-treeview class="projects-view" :items="projects"></v-treeview>
    <v-spacer></v-spacer>
    <v-divider></v-divider>
    <div class="project-settings-panel"></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class ProjectList extends Vue {
  private projects = [
    { id: 1, name: "Project1", children: [{ id: 2, name: "file1" }] },
    { id: 3, name: "Project2" },
  ]; //todo define projects interface
}
</script>

<style scoped>
.projects-panel {
  background-color: var(--v-bg_tertiary-base);
  border: var(--v-bg_tertiary-base) solid 0 !important;
  border-bottom-left-radius: 5px !important;
  border-top-left-radius: 5px !important;
  padding-right: 11px;
}

.project-settings-panel {
  align-self: flex-end;
  height: 100px;
}
</style>
