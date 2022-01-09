<template>
  <div :class="'project-tree ' + (active ? 'project-tree-active' : '')">
    <folder
      class="d-flex flex-column"
      :project="project"
      :fileStates="project.files"
      :folderName="project.settings.data.name"
      :isExpanded="true"
      :isRoot="true"
      :isDeletable="active && !lastProject"
      :isInActiveProject="active"
      :isClickable="!active"
      @click-folder="setActive"
      v-on="$listeners"
    ></folder>
    <div v-if="active && project.settings.data.projectId != ''">
      <v-divider style="margin: 0 0.6em"></v-divider>
      <upload-file-dialog
        :projectId="project.settings.data.projectId"
        v-on="$listeners"
      ></upload-file-dialog>
    </div>
  </div>
</template>

<script lang="ts">
import { apiAddress } from "@/services/BackendAPI";
import { Component, Prop, Vue } from "vue-property-decorator";
import { Project } from "../types/interfaces";

import Folder from "./Folder.vue";
import UploadFileDialog from "@/components/UploadFileDialog.vue";

@Component({
  components: {
    Folder,
    UploadFileDialog,
  },
})
export default class ProjectTreeView extends Vue {
  name = "ProjectTreeView";

  @Prop({ default: false }) active!: boolean;
  @Prop({ default: false }) lastProject!: boolean;
  @Prop({
    default: {
      settings: {
        data: {
          name: "New Project",
          projectId: "",
          projectUrl: new URL(apiAddress),
          sourcesUrl: new URL(apiAddress),
          lintUrl: new URL(apiAddress),
        },
        language: "",
        linter: "",
      },
      files: [],
      openFiles: [],
      activeFile: 0,
    },
  })
  project!: Project;

  private setActive() {
    this.$emit("request-active", this.project.settings.data.projectId);
  }
}
</script>

<style scoped>
.project-tree {
  /*margin: 0.2em 0.5em;*/
  margin: 0.2em 0;
  background-color: transparent;
  border-radius: 5px;
  padding: 0.5em 0;
  transition: background-color 0.1s;
}

.project-tree-active {
  background-color: var(--v-bg_secondary-base);
  transition: background-color 0.2s;
}
</style>
