<template>
  <div class="d-flex flex-column main-content-pane projects-panel">
    <div class="projects-container">
      <project-tree-view
        v-for="(project, index) of projects"
        :key="project.settings.data.projectId"
        :active="index == activeProject"
        :lastProject="projects.length == 1"
        :project="project"
        @request-active="emitSetActiveProject($event)"
        v-on="$listeners"
      ></project-tree-view>
    </div>
    <v-divider class="centered-divider"></v-divider>
    <v-btn
      class="add-project-button"
      text
      color="primary"
      elevation="0"
      @click="$emit('create-project')"
    >
      <v-icon left>mdi-plus</v-icon> Create Project
    </v-btn>

    <v-spacer></v-spacer>
    <div class="active-project-label">
      <span style="color: gray; font-size: smaller">Active Project</span><br />
      {{ projects[activeProject].settings.data.name }}
    </div>
    <v-divider></v-divider>
    <settings-panel v-on="$listeners"></settings-panel>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import SettingsPanel from "@/components/SettingsPanel.vue";
import ProjectTreeView from "@/components/file_tree/ProjectTreeView.vue";
import { Project } from "./types/interfaces";

@Component({
  components: {
    SettingsPanel,
    ProjectTreeView,
  },
})
export default class ProjectList extends Vue {
  @Prop() projects!: Project[];
  @Prop({ default: 0 }) activeProject!: number;
  private internalIdentifier = 0;

  private emitSetActiveProject(projectId: string): void {
    this.projects.forEach((project, index) => {
      if (project.settings.data.projectId == projectId) {
        this.$emit("set-active-project", index);
        return;
      }
    });
  }
}
</script>

<style scoped>
.projects-panel {
  min-width: 250px;
  width: fit-content;
  background-color: var(--v-bg_tertiary-base);
  border: var(--v-bg_tertiary-base) solid 0 !important;
  border-bottom-left-radius: 5px !important;
  border-top-left-radius: 5px !important;
  padding-top: 0.3em;
}

.projects-container {
  min-width: 238px;
  width: fit-content;
  margin-left: 12px;
  padding: 0;
  border-radius: 0;
  overflow-y: scroll;
  scrollbar-color: var(--v-bg_tertiary-lighten1) var(--v-bg_tertiary-base);
  border-bottom-right-radius: 50px;
}

.active-project-label {
  text-align: center;
  color: var(--v-primary-base);
  margin-bottom: 0.3em;
}

.centered-divider {
  margin: 0.4em 10%;
}

.add-project-button {
  margin: 0.2em 12px;
  margin-bottom: 3em;
  flex-grow: 0;
}
</style>
