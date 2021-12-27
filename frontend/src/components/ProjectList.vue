<template>
  <div class="d-flex flex-column main-content-pane projects-panel">
    <v-treeview class="projects-view" :items="projectTrees"></v-treeview>
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
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import SettingsPanel from "@/components/SettingsPanel.vue";
import { Project, ProjectTreeEntry } from "./types/interfaces";

@Component({
  components: {
    SettingsPanel,
  },
})
export default class ProjectList extends Vue {
  @Prop() projects!: Project[];
  private projectTrees: ProjectTreeEntry[] = [
    { id: 1, name: "New Project", children: [{ id: 2, name: "unnamed" }] },
  ];
  private internalIdentifier = 0;

  @Watch("projects")
  createProjectTrees(): void {
    const newTree: ProjectTreeEntry[] = [];
    for (const project of this.projects) {
      let newProject: ProjectTreeEntry = {
        id: this.internalIdentifier++,
        name: project.settings.data.name,
        children: [],
      };
      for (const fileState of project.files) {
        if (newProject.children != undefined) {
          //it should never be undefined because we set it to empty array, but typescript wants this checked because the interface may leave it undefined
          newProject.children.push({
            id: this.internalIdentifier++,
            name: fileState.file.name,
          });
          //TODO this doesn't support recursive children / folder structures
        }
      }
      newTree.push(newProject);
    }
    this.projectTrees = newTree;

    this.internalIdentifier++;
  }
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

.active-project-label {
  text-align: center;
  color: var(--v-primary-base);
  margin-bottom: 0.3em;
}
</style>
