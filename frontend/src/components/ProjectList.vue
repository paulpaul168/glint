<template>
  <div class="d-flex flex-column main-content-pane projects-panel">
    <project-tree-view
      v-for="(project, index) of projects"
      :key="project.settings.data.projectId"
      :active="index == activeProject"
      :lastProject="projects.length == 1"
      :project="project"
      @request-active="emitSetActiveProject($event)"
    ></project-tree-view>
    <v-spacer></v-spacer>
    <div class="active-project-label">
      <span style="color: gray; font-size: smaller">Active Project</span><br />
      {{ projects[0].settings.data.name }}
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
  background-color: var(--v-bg_tertiary-base);
  border: var(--v-bg_tertiary-base) solid 0 !important;
  border-bottom-left-radius: 5px !important;
  border-top-left-radius: 5px !important;
  padding-right: 12px;
  padding-top: 0.3em;
}

.active-project-label {
  text-align: center;
  color: var(--v-primary-base);
  margin-bottom: 0.3em;
}
</style>
