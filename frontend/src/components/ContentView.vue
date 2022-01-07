<template>
  <div class="main-content-pane" style="margin-right: 15px">
    <div
      style="height: 100%; padding: 0 12px"
      v-if="project.contentViewMode == 'files'"
    >
      <v-row style="margin-top: 0">
        <v-tabs
          v-model="project.activeFile"
          show-arrows
          class="file-tabs"
          background-color="bg_tertiary"
        >
          <v-tab
            class="file-tab"
            v-for="(state, index) in internalProject.openFiles"
            :key="state.id"
          >
            <file-tab
              :title="state.file.name"
              :unsaved="state.unsaved"
              :active="project.activeFile == index"
              @file-close="closeFile"
              @file-rename="renameFile"
            ></file-tab>
          </v-tab>
        </v-tabs>
      </v-row>
      <v-row style="height: calc(100% - 48px)">
        <v-tabs-items
          v-model="project.activeFile"
          class="main-file-view"
          justify="center"
          align="center"
        >
          <v-tab-item
            style="height: 100%"
            v-for="state in internalProject.openFiles"
            :key="state.id"
          >
            <v-toolbar
              v-if="
                internalProject.filesViewMode == 'source' ||
                internalProject.filesViewMode == 'lint'
              "
              class="toolbar"
              dense
              elevation="0"
              color="transparent"
            >
              <v-tooltip v-if="state.unsaved" bottom open-delay="1000">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="toolbar-element"
                    small
                    elevation="0"
                    color="transparent"
                    v-bind="attrs"
                    v-on="on"
                    :loading="uploading"
                    @click="saveFile"
                  >
                    <v-icon small>mdi-content-save</v-icon>
                  </v-btn>
                </template>
                <span>Send File to Server</span>
              </v-tooltip>
              <v-tooltip
                v-if="lintOutdated && project.lintData.status != 'processing'"
                bottom
                open-delay="1000"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="toolbar-element"
                    small
                    elevation="0"
                    color="transparent"
                    v-bind="attrs"
                    v-on="on"
                    :loading="
                      project.lintData.status == 'processing' &&
                      project.remainingLintChecks > 0
                    "
                    @click="$emit('request-new-lint')"
                  >
                    <v-icon small>mdi-cached</v-icon>
                  </v-btn>
                </template>
                <span>Request new Lint</span>
              </v-tooltip>
              <v-tooltip
                v-if="project.lintData.status"
                bottom
                open-delay="1000"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="toolbar-element"
                    small
                    elevation="0"
                    color="transparent"
                    v-bind="attrs"
                    v-on="on"
                    :loading="
                      project.lintData.status == 'processing' &&
                      project.remainingLintChecks > 0
                    "
                    :disabled="
                      !(
                        project.lintData.status == 'done' ||
                        project.lintData.status == 'processing'
                      )
                    "
                    @click="handleLintSwitcher"
                  >
                    <v-icon
                      v-if="internalProject.filesViewMode == 'lint'"
                      small
                    >
                      mdi-pencil
                    </v-icon>
                    <v-icon
                      v-else-if="
                        internalProject.filesViewMode == 'source' &&
                        project.lintData.status == 'done'
                      "
                      small
                    >
                      mdi-format-list-bulleted
                    </v-icon>
                    <v-icon
                      v-else-if="
                        internalProject.filesViewMode == 'source' &&
                        project.lintData.status == 'processing' &&
                        project.remainingLintChecks <= 0
                      "
                      small
                    >
                      mdi-reload
                    </v-icon>
                    <v-icon
                      v-else-if="
                        project.lintData.status != 'done' &&
                        project.lintData.status != 'processing'
                      "
                      small
                    >
                      mdi-alert-circle
                    </v-icon>
                  </v-btn>
                </template>
                <span v-if="internalProject.filesViewMode == 'lint'">
                  Show Source
                </span>
                <span
                  v-else-if="
                    internalProject.filesViewMode == 'source' &&
                    project.lintData.status == 'processing' &&
                    project.remainingLintChecks <= 0
                  "
                >
                  Retry fetching Lint result
                </span>
                <span v-if="internalProject.filesViewMode == 'source'">
                  Show Lint
                </span>
              </v-tooltip>
            </v-toolbar>
            <lint-view
              v-if="internalProject.filesViewMode == 'lint'"
              :fileState="state"
              :outdated="lintOutdated"
              :linter="
                internalProject.lintData.linters[
                  state.language == 'auto'
                    ? state.detectedLanguage
                    : state.language
                ]
              "
              :lints="lintsByFile[state.file.name]"
              @go-to-source="openFileAt($event)"
            ></lint-view>
            <code-view
              v-if="
                internalProject.filesViewMode == 'source' ||
                internalProject.filesViewMode == 'uploader'
              "
              :fileState="state"
              :language="
                state.language == 'auto'
                  ? state.detectedLanguage
                  : state.language
              "
              @input="codeEdited"
            ></code-view>
            <upload-dialog
              v-if="internalProject.filesViewMode == 'uploader'"
              :uploading="uploading"
              v-on="$listeners"
            ></upload-dialog>
            <file-footer
              v-if="internalProject.filesViewMode == 'source'"
              :language="state.language"
              :languageLabel="state.detectedLanguage"
              @language-set="changeLanguage($event)"
            ></file-footer>
          </v-tab-item>
          <div
            v-if="
              internalProject.openFiles == 0 &&
              project.contentViewMode == 'files'
            "
            style="height: 100%"
          >
            <h2 style="position: relative; top: 45%">No Files are open</h2>
          </div>
        </v-tabs-items>
      </v-row>
    </div>
    <project-overview
      v-if="project.contentViewMode == 'overview'"
      :project="project"
      :searchPatterns="searchPatterns"
      :searchResults="searchResults"
      v-on="$listeners"
    ></project-overview>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";

import * as API from "@/services/BackendAPI";
import UploadDialog from "@/components/UploadDialog.vue";
import CodeView from "@/components/CodeView.vue";
import LintView from "@/components/LintView.vue";
import FileTab from "@/components/FileTab.vue";
import FileFooter from "@/components/FileFooter.vue";
import ProjectOverview from "@/components/ProjectOverview.vue";

import {
  FileState,
  GoToFileEvent,
  Lint,
  Project,
  SearchPatterns,
  SearchResult,
} from "./types/interfaces";
import { getLanguage } from "@/services/LanguageDetection";
import { Dictionary } from "vue-router/types/router";

@Component({
  components: {
    UploadDialog,
    CodeView,
    LintView,
    FileTab,
    FileFooter,
    ProjectOverview,
  },
})
export default class ContentView extends Vue {
  name = "ContentView";
  @Prop({ default: false }) uploading!: boolean;
  @Prop() project!: Project;
  @Prop() searchPatterns!: SearchPatterns;
  @Prop() searchResults!: Dictionary<SearchResult[]>;
  private internalProject: Project = {
    settings: {
      data: {
        name: "No Project",
        projectId: "1",
        projectUrl: new URL(API.apiAddress),
        sourcesUrl: new URL(API.apiAddress),
        lintUrl: new URL(API.apiAddress),
      },
      linters: {},
    },
    files: [],
    openFiles: [
      {
        id: 0,
        edited: false,
        unsaved: false,
        language: "auto",
        detectedLanguage: "txt",
        file: { name: "unnamed", path: "unnamed", content: "" },
      },
    ],
    lintData: {
      status: "",
      linters: {},
      lintFiles: [],
    },
    contentViewMode: "files",
    filesViewMode: "uploader",
    remainingLintChecks: 5,
  };

  private lintsByFile: Dictionary<Lint[]> = { none: [] };
  private lintOutdated = false;

  //this may need to be converted into a deep watcher, but for now I'll try not to as it makes the code a bit nicer and tidier if only a few things within a project change without the entire project being replaced
  @Watch("project")
  projectChanged(): void {
    console.log("project changed");
    this.internalProject = { ...this.project };
    //this.convertLintsToDict();
    //this.filesChanged();
    //this.selectViewMode();
  }

  @Watch("project.files")
  private filesChanged(): void {
    this.internalProject.files = [];
    for (const state of this.project.files) {
      console.log("file");
      const newState: FileState = {
        file: {
          name: "",
          path: "",
          content: "",
        },
        language: "auto",
        detectedLanguage: "",
        unsaved: false,
        edited: false,
      };
      newState.file.name = (" " + state.file.name).slice(1);
      newState.file.path = (" " + state.file.path).slice(1);
      newState.file.content = (" " + state.file.content).slice(1);
      newState.language = (" " + state.language).slice(1);
      newState.detectedLanguage = (" " + state.detectedLanguage).slice(1);
      this.internalProject.files.push(newState);
    }
  }

  @Watch("project.openFiles")
  private openFilesChanged(): void {
    console.log("open file change");
    this.internalProject.openFiles = [];
    this.project.openFiles?.forEach((state) => {
      const newState: FileState = {
        file: {
          name: "",
          path: "",
          content: "",
        },
        language: "auto",
        detectedLanguage: "",
        unsaved: false,
        edited: false,
      };
      newState.file.name = (" " + state.file.name).slice(1);
      newState.file.path = (" " + state.file.path).slice(1);
      newState.file.content = (" " + state.file.content).slice(1);
      newState.language = (" " + state.language).slice(1);
      newState.detectedLanguage = (" " + state.detectedLanguage).slice(1);
      this.internalProject.openFiles?.push(newState);
    });
    this.selectViewMode();
    //I don't like having selectViewMode here - a while ago the watch project.files triggered before
    //watch project, if this happens again but with project.openFiles this will break
  }

  //consider moving the individual watchers into the "main" watcher (may increase code runtime but makes it a bit simpler?)
  @Watch("project.lintData")
  convertLintsToDict(): void {
    console.log("lint changed");
    //convert the array of lints of various files into a dict with one entry of many lints per file
    for (const lintFile of this.project.lintData.lintFiles) {
      this.lintsByFile[lintFile.name] = lintFile.lints;
    }
    this.lintOutdated = false;
  }

  @Watch("project.activeFile")
  private activeFileChanged(): void {
    this.internalProject.activeFile = this.project.activeFile;
  }

  private setLintOutdated(): void {
    if (this.lintsByFile != { none: [] }) {
      this.lintOutdated = true;
    }
  }

  private selectViewMode(): void {
    if (this.project.filesViewMode == "auto") {
      if (this.internalProject.settings.data.projectId == "") {
        if (this.internalProject.files.length == 0) {
          this.internalProject.filesViewMode = "uploader";
          this.internalProject.openFiles = [
            {
              id: 0,
              edited: false,
              unsaved: false,
              language: "auto",
              detectedLanguage: "txt",
              file: { name: "unnamed", path: "unnamed", content: "" },
            },
          ];
          console.log("set open files");
        } else {
          console.log(
            "files:",
            this.internalProject.files.length,
            this.internalProject.files[0].file.name
          );
          this.$emit("notification", {
            type: "error",
            message:
              "Encountered project without any ID set but that contains files. Only empty projects are allowed to have no ID!",
          });
        }
      } else {
        this.internalProject.filesViewMode = "source";
      }
      this.$emit("files-view-change", this.internalProject.filesViewMode);
    } else {
      if (this.project.filesViewMode == "uploader") {
        this.internalProject.openFiles = [
          {
            id: 0,
            edited: false,
            unsaved: false,
            language: "auto",
            detectedLanguage: "txt",
            file: { name: "unnamed", path: "unnamed", content: "" },
          },
        ];
      }
      this.internalProject.filesViewMode = this.project.filesViewMode;
    }
  }

  private changeLanguage(newLanguage: string) {
    const activeTab = this.internalProject.activeFile as number;
    (this.internalProject.openFiles as FileState[])[activeTab].language =
      newLanguage;
    let detectedLanguage = "txt";
    detectedLanguage = getLanguage(
      this.internalProject.openFiles?.[activeTab].file.name
    );
    (this.internalProject.openFiles as FileState[])[
      activeTab
    ].detectedLanguage = detectedLanguage;

    this.internalProject.files.forEach((state, index) => {
      if (
        state.file.path == this.internalProject.openFiles?.[activeTab].file.path
      ) {
        this.internalProject.files[index].language = newLanguage;
        this.internalProject.files[index].detectedLanguage = detectedLanguage;
        return;
      }
    });
    this.$emit("open-files-change", {
      openFiles: this.internalProject.openFiles,
      activeFile: this.internalProject.activeFile,
    });
    //TODO investigate: why do I need to set files languages and not just openFiles? do I even need to? If I do need to set files, I need to emit files-change not open-files-change, but this also triggers a file upload. maybe add a flag whether to upload or not?
  }

  private openFileAt(event: GoToFileEvent): void {
    //find the file that should be opened
    this.internalProject.openFiles?.forEach((state, index) => {
      //this assumes the file is present in the open files list, I don't see a way how this is not the case as only open files show lint view, but dunno, maybe this will create bugs
      if (state.file.path == event.filePath) {
        this.internalProject.activeFile = index;
        //TODO: jumping to (and highlighting?) line
        //TODO: switching to source view
      }
    });
  }

  private codeEdited(): void {
    if (this.internalProject.filesViewMode == "uploader") {
      this.internalProject.filesViewMode = "source"; //TODO probably more to do here once that happens (someone writing in an empty file while the upload button is showing)
      this.$emit("files-view-change", this.internalProject.filesViewMode);
    }
    (this.internalProject.openFiles as FileState[])[
      this.internalProject.activeFile as number
    ].edited = true;
    (this.internalProject.openFiles as FileState[])[
      this.internalProject.activeFile as number
    ].unsaved = true;

    this.$emit("open-files-change", {
      openFiles: this.internalProject.openFiles,
      activeFile: this.internalProject.activeFile,
    });
    //TODO consider moving event emit away from here or change to more barebones file-edit event (each typed char moves the entire file data around) and maybe add a getChanges public function for Home.vue to call to read on project context switch
  }

  private async saveFile(): Promise<void> {
    this.setLintOutdated();
    const activeTab = this.internalProject.activeFile as number;
    this.internalProject.files.forEach((state, index) => {
      if (
        state.file.path == this.internalProject.openFiles?.[activeTab].file.path
      ) {
        const fileToSave: FileState = {
          file: {
            name: "",
            path: "",
            content: "",
          },
          language: "auto",
          detectedLanguage: "",
          unsaved: false,
          edited: false,
        };
        fileToSave.file.name = (
          " " + this.internalProject.openFiles?.[activeTab].file.name
        ).slice(1);
        fileToSave.file.path = (
          " " + this.internalProject.openFiles?.[activeTab].file.path
        ).slice(1);
        fileToSave.file.content = (
          " " + this.internalProject.openFiles?.[activeTab].file.content
        ).slice(1);
        fileToSave.language = (
          " " + this.internalProject.openFiles?.[activeTab].language
        ).slice(1);
        fileToSave.detectedLanguage = (
          " " + this.internalProject.openFiles?.[activeTab].detectedLanguage
        ).slice(1);
        this.internalProject.files[index] = fileToSave;
      }
    });

    this.$emit("files-change", {
      files: this.internalProject.files,
      openFiles: this.internalProject.openFiles,
      activeFile: this.internalProject.activeFile,
    });
  }

  private closeFile(): void {
    let activeTab = this.internalProject.activeFile as number;
    console.log("cur active", activeTab);
    this.internalProject.openFiles?.splice(activeTab, 1);
    if (activeTab >= (this.internalProject.openFiles as FileState[]).length) {
      //if the last file in the list was active and then closed the activeTab index is out of boudns
      activeTab = (this.internalProject.openFiles as FileState[]).length - 1;
      if (activeTab < 0) {
        activeTab = 0;
      }
      this.internalProject.activeFile = activeTab;
      console.log("new active", activeTab);
    }
    this.$emit("open-files-change", {
      openFiles: this.internalProject.openFiles,
      activeTab,
    });
    //TODO if unsaved ask if it really should be closed?
  }

  private renameFile(name: string): void {
    //TODO this doesn't handle path changes on the rename yet
    const activeTab = this.internalProject.activeFile as number;
    const oldPath = this.internalProject.openFiles?.[activeTab].file.path;

    (this.internalProject.openFiles as FileState[])[activeTab].file.name = name;
    (this.internalProject.openFiles as FileState[])[activeTab].file.path =
      oldPath?.substring(0, oldPath.lastIndexOf("/")) + name;
    (this.internalProject.openFiles as FileState[])[activeTab].unsaved = true;
    this.$emit("rename-file", {
      openFiles: this.internalProject.openFiles,
      activeFile: activeTab,
    });

    /*this.internalProject.files.forEach((state, index) => {
      if (state.file.name == oldName) {
        this.internalProject.files[index].file.name = name;
        return;
      }
    });*/
  }

  private handleLintSwitcher(): void {
    if (this.project.lintData.status == "done") {
      if (this.internalProject.filesViewMode == "source") {
        this.internalProject.filesViewMode = "lint";
      } else if (this.internalProject.filesViewMode == "lint") {
        this.internalProject.filesViewMode = "source";
      }
      this.$emit("files-view-change", this.internalProject.filesViewMode);
    } else if (
      this.project.lintData.status == "processing" &&
      (this.project.remainingLintChecks || 0) <= 0
    ) {
      this.$emit("retry-get-lint");
      //this.remainingLintChecks = 3;
      //this.lintCheckTimer = setInterval(this.handleLintTimer, 1000);
    }
  }
}
</script>

<style scoped>
.file-tabs {
  background-color: var(--v-bg_tertiary-base);
  border: var(--v-bg_secondary-base) solid 0px;
  border-top-right-radius: 5px !important;
}

.file-tab {
  text-transform: none;
  flex-flow: column;
}

.main-file-view {
  width: 100%;
  height: 100%;

  border: var(--v-bg_secondary-base) solid 0 !important;
  border-bottom-right-radius: 5px !important;
}

.toolbar {
  position: absolute;
  right: 0.1em;
  z-index: 10;
}

.toolbar-element {
  margin-left: 0.2em;
  min-width: 43px !important;
}
</style>
