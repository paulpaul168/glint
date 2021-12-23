<template>
  <div class="d-flex flex-column main-content-pane projects-panel">
    <v-treeview class="projects-view" :items="projectTrees"></v-treeview>
    <v-spacer></v-spacer>
    <v-divider></v-divider>
    <project-settings v-on="$listeners"></project-settings>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import ProjectSettings from "@/components/ProjectSettings.vue";
import { Project, ProjectTreeEntry } from "./types/interfaces";

@Component({
  components: {
    ProjectSettings,
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
</style>
