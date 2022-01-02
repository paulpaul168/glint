<template>
  <div class="main-content-pane" style="margin-right: 15px">
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
            v-if="viewMode == 'source' || viewMode == 'lint'"
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
            <v-tooltip v-if="project.lintData.status" bottom open-delay="1000">
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
                      (project.lintData.status == 'processing' &&
                        project.remainingLintChecks == 0)
                    )
                  "
                  @click="handleLintSwitcher"
                >
                  <v-icon v-if="viewMode == 'lint'" small>mdi-pencil</v-icon>
                  <v-icon
                    v-else-if="
                      viewMode == 'source' && project.lintData.status == 'done'
                    "
                    small
                  >
                    mdi-format-list-bulleted
                  </v-icon>
                  <v-icon
                    v-else-if="
                      viewMode == 'source' &&
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
              <span v-if="viewMode == 'lint'">Show Source</span>
              <span
                v-else-if="
                  viewMode == 'source' &&
                  project.lintData.status == 'processing' &&
                  project.remainingLintChecks <= 0
                "
              >
                Retry fetching Lint result
              </span>
              <span v-if="viewMode == 'source'">Show Lint</span>
            </v-tooltip>
          </v-toolbar>
          <lint-view
            v-if="viewMode == 'lint'"
            :fileState="state"
            :lints="lintsByFile[state.file.name]"
          ></lint-view>
          <code-view
            v-if="viewMode == 'source'"
            :fileState="state"
            :language="
              state.language == 'auto' ? state.detectedLanguage : state.language
            "
            @input="codeEdited"
          ></code-view>
          <upload-dialog
            v-if="viewMode == 'uploader'"
            :uploading="uploading"
            v-on="$listeners"
          ></upload-dialog>
          <file-footer
            v-if="viewMode == 'source'"
            :language="state.language"
            :languageLabel="state.detectedLanguage"
            @language-set="changeLanguage($event)"
          ></file-footer>
        </v-tab-item>
        <div
          v-if="
            internalProject.openFiles == 0 &&
            internalProject.viewMode == 'files'
          "
          style="height: 100%"
        >
          <h2 style="position: relative; top: 45%">No Files are open</h2>
        </div>
      </v-tabs-items>
    </v-row>
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

import { FileState, Lint, Project } from "./types/interfaces";
import { getLanguage } from "@/services/LanguageDetection";
import { Dictionary } from "vue-router/types/router";

@Component({
  components: {
    UploadDialog,
    CodeView,
    LintView,
    FileTab,
    FileFooter,
  },
})
export default class ContentView extends Vue {
  name = "ContentView";
  @Prop({ default: false }) uploading!: boolean;
  @Prop() project!: Project;
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
    viewMode: "files",
    remainingLintChecks: 5,
  };
  private viewMode = "uploader"; //which state the UI is in, can be "uploader" = empty with upload "+" button, "source" = show project source, "lint" = show lint results, "project" = show project spanning data like stats and found secrets

  private lintsByFile: Dictionary<Lint[]> = { none: [] };
  private fileIdCounter = 0;

  //this may need to be converted into a deep watcher, but for now I'll try not to as it makes the code a bit nicer and tidier if only a few things within a project change without the entire project being replaced
  @Watch("project")
  projectChanged(): void {
    console.log("project changed");
    //I may need to also store openFileStates in the project data so switching back and forth is more seamless (otherwise it loses list of open vs closed files, active file etc)
    this.internalProject = this.project;
    this.lintsByFile = { none: [] };
    //this.filesChanged();
    this.selectViewMode();
  }

  @Watch("project.files")
  private filesChanged(): void {
    console.log("files changed!");
    /*setTimeout(() => {
      this.selectViewMode();
    }, 100);*/
    //TODO iterate through all files from project prop, compare with files in internalProject and update as necessary. If we just copy the entire thing over
    this.internalProject.files = this.project.files;
  }

  @Watch("project.openFiles")
  private openFilesChanged(): void {
    this.internalProject.openFiles = this.project.openFiles;
  }

  @Watch("project.activeFile")
  private activeFileChanged(): void {
    this.internalProject.activeFile = this.project.activeFile;
  }

  private selectViewMode(): void {
    if (this.internalProject.settings.data.projectId == "") {
      console.log("id:", this.internalProject.settings.data.projectId);
      if (this.internalProject.files.length == 0) {
        this.viewMode = "uploader";
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
      } else {
        console.log(
          "files:",
          this.internalProject.files.length,
          this.internalProject.files[0].file.name
        );
        this.$emit("notification", {
          type: "error",
          message:
            "Encountered Project without any ID set but that contains files. Only empty projects are allowed to have no ID!",
        });
      }
    } else {
      this.viewMode = "source";
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

  //consider moving the individual watchers into the "main" watcher (may increase code runtime but makes it a bit simpler?)
  @Watch("project.lintData")
  convertLintsToDict(): void {
    //convert the array of lints of various files into a dict with one entry of many lints per file
    for (const lintFile of this.project.lintData.lintFiles) {
      this.lintsByFile[lintFile.name] = lintFile.lints;
    }
  }

  private codeEdited(): void {
    if (this.viewMode == "uploader") {
      this.viewMode = "source"; //TODO probably more to do here once that happens (someone writing in an empty file while the upload button is showing)
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
    //this.uploading = true;
    const activeTab = this.internalProject.activeFile as number;
    this.internalProject.files.forEach((state, index) => {
      if (
        state.file.path == this.internalProject.openFiles?.[activeTab].file.path
      ) {
        this.internalProject.files[index] =
          this.internalProject.openFiles?.[activeTab];
      }
    });

    this.$emit("files-change", {
      files: this.internalProject.files,
      openFiles: this.internalProject.openFiles,
      activeFile: this.internalProject.activeFile,
    });
    /*let result = await API.overwriteFile(
      this.project.settings.data.projectId,
      this.openFileStates[this.activeTab].file
    );
    if (result.success == false) {
      this.$emit("notification", {
        type: "error",
        message: result.errorMessage,
      });
      this.uploading = false;
      return;
    }
    this.uploading = false;
    this.openFileStates[this.activeTab].unsaved = false;
    this.$emit("file-edit", this.openFileStates[this.activeTab]);*/
    return;
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
    const oldName = this.internalProject.openFiles?.[activeTab].file.name;
    (this.internalProject.openFiles as FileState[])[activeTab].file.name = name;
    this.internalProject.files.forEach((state, index) => {
      if (state.file.name == oldName) {
        this.internalProject.files[index].file.name = name;
        return;
      }
    });
    (this.internalProject.openFiles as FileState[])[activeTab].unsaved = true;
  }

  private handleLintSwitcher(): void {
    if (this.project.lintData.status == "done") {
      if (this.viewMode == "source") {
        this.viewMode = "lint";
      } else if (this.viewMode == "lint") {
        this.viewMode = "source";
      }
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
