<template>
  <div
    :class="
      isRoot ? (internalIsExpanded ? 'padding-open' : 'padding-close') : ''
    "
  >
    <div style="margin: 0 0.4em" class="d-flex flex-row">
      <v-btn
        icon
        :ripple="false"
        :disabled="files.length + Object.keys(folders).length < 1"
        @click="toggleFolderExpansion"
      >
        <v-icon
          :style="
            files.length + Object.keys(folders).length < 1
              ? 'visibility: hidden'
              : ''
          "
          :class="internalIsExpanded ? 'chevron-open' : 'chevron-close'"
          small
        >
          mdi-chevron-right
        </v-icon>
      </v-btn>
      <v-btn
        :class="
          'folder-name text-body-1 ' +
          (isRoot ? '' : isClickable ? '' : 'disable-button')
        "
        text
        :ripple="false"
        @click="clickFolder"
      >
        {{ folderName }}
      </v-btn>
      <v-tooltip right open-delay="1000">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            :ripple="false"
            v-bind="attrs"
            v-on="on"
            :disabled="!isDeletable"
            @click="$emit('close-project')"
          >
            <v-icon v-if="isDeletable" small>mdi-close</v-icon>
          </v-btn>
        </template>
        <span>Close Project</span>
      </v-tooltip>
    </div>
    <div style="width: 100%" class="d-flex flex-row">
      <v-expand-transition>
        <div v-show="internalIsExpanded" class="folder-collapsible">
          <folder
            v-for="(state, name) in folders"
            :key="name"
            :project="project"
            :fileStates="state"
            :folderTree="folderTree + name + '/'"
            :folderName="name"
            :isInActiveProject="isInActiveProject"
            :isClickable="false"
            :isRoot="false"
            @open-file="handleFileClick($event)"
            @delete-file="handleFileDelete($event)"
          ></folder>
          <file
            v-for="(state, index) of files"
            :key="index"
            class="file"
            :state="state"
            :project="project"
            :folderTree="folderTree"
            :active="
              (project.openFiles[project.activeFile] != undefined
                ? project.openFiles[project.activeFile].file.path
                : ''
              ).replace(folderTree, '') == state.file.path && isInActiveProject
            "
            @open-file="handleFileClick($event)"
            @delete-file="handleFileDelete($event)"
          ></file>
        </div>
      </v-expand-transition>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { Dictionary } from "vue-router/types/router";
import { FileState, GoToFileEvent, Project } from "../types/interfaces";
import File from "./File.vue";

@Component({
  components: {
    File,
  },
})
export default class Folder extends Vue {
  name = "Folder";
  @Prop() project!: Project;
  @Prop({ default: "" }) folderTree!: string;
  @Prop({ default: "<folder name>" }) folderName!: string;
  @Prop() fileStates!: FileState[];
  @Prop({ default: false }) isRoot!: boolean;
  @Prop({ default: false }) isInActiveProject!: boolean;
  @Prop({ default: true }) isExpanded!: boolean;
  @Prop({ default: false }) isDeletable!: boolean;
  @Prop({ default: true }) isClickable!: boolean;

  private internalIsExpanded = false;

  //folders to display including any child data they may need to display
  private folders: Dictionary<FileState[]> = {};

  //files to display
  private files: FileState[] = [];

  created(): void {
    this.expandedChange();
    this.extractDisplayData();
    if (this.files.length + Object.keys(this.folders).length < 1) {
      //needed to collapse an empty project as that shows no arrow to do so
      this.internalIsExpanded = false;
    }
  }

  @Watch("isExpanded")
  private expandedChange(): void {
    this.internalIsExpanded = this.isExpanded;
  }

  @Watch("project")
  @Watch("fileStates")
  private extractDisplayData(): void {
    this.folders = {};
    this.files = [];
    for (const state of this.fileStates) {
      const pathParts = state.file.path.split("/");
      if (pathParts == undefined || pathParts.length <= 1) {
        this.files.push(state);
      } else {
        const subState: FileState = {
          file: {
            name: (" " + state.file.name).slice(1),
            path: (" " + state.file.path).slice(1),
            content: state.file.content,
          },
          language: state.language,
          detectedLanguage: state.detectedLanguage,
          unsaved: state.unsaved,
          edited: state.edited,
        };
        subState.file.path = subState.file.path.substring(
          subState.file.path.indexOf("/") + 1
        ); //remove the highest level folder (this folder) from path before passing on
        if (this.folders[pathParts[0]] == undefined) {
          this.folders[pathParts[0]] = [];
        }
        this.folders[pathParts[0]].push(subState);
      }
    }
  }

  private handleFileClick(clickedFile: GoToFileEvent): void {
    if (!this.isRoot) {
      //if the folder is not the root folder, add the folder name to the path of the file before re-emitting
      const newClickEvent: GoToFileEvent = {
        filePath: this.folderName + "/" + clickedFile.filePath,
        projectId: clickedFile.projectId,
      };

      this.$emit("open-file", newClickEvent);
      return;
    }
    this.$emit("open-file", clickedFile);
    return;
  }

  private handleFileDelete(fileToDelete: GoToFileEvent): void {
    if (!this.isRoot) {
      //if the folder is not the root folder, add the folder name to the path of the file before re-emitting
      const newClickEvent: GoToFileEvent = {
        filePath: this.folderName + "/" + fileToDelete.filePath,
        projectId: fileToDelete.projectId,
      };

      this.$emit("delete-file", newClickEvent);
      return;
    }
    this.$emit("delete-file", fileToDelete);
    return;
  }

  private clickFolder(): void {
    if (this.isInActiveProject) {
      if (this.isRoot) {
        this.$emit("toggle-project-info");
      }
    } else {
      this.$emit("click-folder");
    }
  }

  private toggleFolderExpansion(): void {
    this.internalIsExpanded = !this.internalIsExpanded;
  }
}
</script>

<style scoped>
.folder-collapsible {
  flex-grow: 1;
  margin-left: 36px;
  margin-right: 0;
  width: fit-content;
}

.folder-name {
  text-transform: none;
  justify-content: left;
  padding-left: 4px !important;
  padding-right: auto !important;
  flex-grow: 1;
}

.folder-name::v-deep .v-btn__content {
  overflow: hidden;
  white-space: nowrap;
  max-width: 300px;
  text-overflow: ellipsis;
  display: inline-block;
  text-align: left;
}

.disable-button {
  pointer-events: none;
}

.chevron-open {
  transform: rotate(90deg);
  transition: 0.3s;
}

.chevron-close {
  transition: 0.2s;
}

.padding-open {
  padding-bottom: 0.3em !important;
  transition: 0.2s;
}

.padding-close {
  padding-bottom: 0.5em !important;
  transition: 0.1s; /* the transition seems to not work properly */
}

.file {
  padding: 0.2em 0;
}
</style>
