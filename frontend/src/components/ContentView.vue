<template>
  <div class="main-content-pane" style="margin-right: 15px">
    <v-row style="margin-top: 0">
      <v-tabs
        v-model="activeTab"
        show-arrows
        class="file-tabs"
        background-color="bg_tertiary"
      >
        <v-tab
          class="file-tab"
          v-for="(state, index) in openFileStates"
          :key="state.id"
        >
          <file-tab
            :title="state.file.name"
            :unsaved="state.unsaved"
            :active="activeTab == index"
            @file-close="closeFile"
            @file-rename="renameFile"
          ></file-tab>
        </v-tab>
        <!--<v-tab v-if="showUploader">
          <v-icon>mdi-plus</v-icon>
        </v-tab>-->
      </v-tabs>
    </v-row>
    <v-row style="height: calc(100% - 48px)">
      <v-tabs-items
        v-model="activeTab"
        class="main-file-view"
        justify="center"
        align="center"
      >
        <v-tab-item
          style="height: 100%"
          v-for="state in openFileStates"
          :key="state.id"
        >
          <v-toolbar class="toolbar" dense elevation="0" color="transparent">
            <v-tooltip bottom open-delay="1000" v-if="state.unsaved">
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
            <v-tooltip bottom open-delay="1000" v-if="lintData.status">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  class="toolbar-element"
                  small
                  elevation="0"
                  color="transparent"
                  v-bind="attrs"
                  v-on="on"
                  :loading="
                    lintData.status == 'processing' && remainingLintChecks > 0
                  "
                  :disabled="
                    !(
                      lintData.status == 'done' ||
                      (lintData.status == 'processing' &&
                        remainingLintChecks == 0)
                    )
                  "
                  @click="handleLintSwitcher"
                >
                  <v-icon small v-if="showLint">mdi-pencil</v-icon>
                  <v-icon
                    small
                    v-else-if="!showLint && lintData.status == 'done'"
                    >mdi-format-list-bulleted</v-icon
                  >
                  <v-icon
                    small
                    v-else-if="
                      !showLint &&
                      lintData.status == 'processing' &&
                      remainingLintChecks <= 0
                    "
                    >mdi-reload</v-icon
                  >
                  <v-icon
                    small
                    v-else-if="
                      lintData.status != 'done' &&
                      lintData.status != 'processing'
                    "
                    >mdi-alert-circle</v-icon
                  >
                </v-btn>
              </template>
              <span v-if="showLint">Show Source</span>
              <span
                v-else-if="
                  !showLint &&
                  lintData.status == 'processing' &&
                  remainingLintChecks <= 0
                "
              >
                Retry fetching Lint result
              </span>
              <span v-else>Show Lint</span>
            </v-tooltip>
          </v-toolbar>
          <lint-view
            v-if="showLint"
            :fileState="state"
            :lints="lintsByFile[state.file.name]"
          ></lint-view>
          <code-view
            v-else
            :fileState="state"
            :language="detectedLanguage"
            @input="codeEdited"
          ></code-view>
          <upload-dialog
            v-if="showUploader"
            :uploading="uploading"
            @file-event="loadProject($event)"
          ></upload-dialog>
        </v-tab-item>
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

import {
  FileEvent,
  FileHandle,
  FileState,
  ProjectData,
  Notification,
  Lint,
} from "./types/interfaces";
import { LintResponse } from "@/services/types/api_responses_interfaces";
import { getLanguage } from "@/services/LanguageDetection";
import { Dictionary } from "vue-router/types/router";

@Component({
  components: {
    UploadDialog,
    CodeView,
    LintView,
    FileTab,
  },
})
export default class ContentView extends Vue {
  name = "ContentView";
  @Prop() language!: string;
  @Prop() linter!: string;
  private showUploader = true;
  private showLint = false;
  private lintCheckTimer!: number;
  private remainingLintChecks = 5;
  private projectData: ProjectData = {
    //the defaults here need to be removed at some point and synced with a separate @Prop projectdata
    data: {
      name: "DefaultProject",
      projectId: "DefaultProject",
      projectUrl: new URL(API.apiAddress), //I dislike these default, I'd love to not have to specify them at all, but I think I might need to because I need language defaults
      sourcesUrl: new URL(API.apiAddress),
      lintUrl: new URL(API.apiAddress),
    },
    language: "auto",
    linter: "auto",
  };
  private detectedLanguage = "txt";
  private lintData: LintResponse = {
    status: "", //processing means lint is ongoing/result hasn't come in yet, done means lint has been received, anything else means error on linting
    linter: "",
    lintFiles: [
      {
        name: "",
        path: "",
        lints: [],
      },
    ],
  };
  private lintsByFile: Dictionary<Lint[]> = { none: [] };
  private activeTab = 0;
  private uploading = false;
  private fileStates: FileState[] = [
    {
      edited: false,
      unsaved: false,
      file: { name: "unnamed", path: "unnamed", content: "" },
    },
  ];
  private openFileStates: FileState[] = [
    {
      id: 0,
      edited: false,
      unsaved: false,
      file: { name: "unnamed", path: "unnamed", content: "" },
    },
  ];
  private fileIdCounter = 0;

  private emitNotification(notification: Notification): void {
    this.$emit("notification", notification);
  }

  @Watch("language")
  private languageChange() {
    this.projectData.language = this.language;
    if (this.projectData.language == "auto") {
      //TODO right now the whole project's language is being read from the first file. this is not great but I don't really know what else to do.
      this.detectedLanguage = getLanguage(this.fileStates[0].file.name);
    } else {
      this.detectedLanguage = this.language;
    }
  }

  @Watch("linter")
  private linterChange() {
    this.projectData.linter = this.linter;
  }

  private codeEdited(): void {
    if (this.showUploader == true) {
      this.showUploader = false; //TODO probably more to do here once that happens (someone writing in an empty file while the upload button is showing)
    }
    this.openFileStates[this.activeTab].edited = true;
    this.openFileStates[this.activeTab].unsaved = true;
  }

  private async saveFile(): Promise<void> {
    this.uploading = true;
    let result = await API.overwriteFile(
      this.projectData.data.projectId,
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
    return;
  }

  private closeFile(): void {
    this.openFileStates.splice(this.activeTab, 1);
    if (this.activeTab >= this.openFileStates.length) {
      //if the last file in the list was active and then closed the activeTab index is out of boudns
      this.activeTab = this.openFileStates.length - 1;
    }
    //TODO if unsaved ask if it really should be closed?
  }

  private renameFile(name: string): void {
    //TODO this doesn't handle path changes on the rename yet
    const oldName = this.openFileStates[this.activeTab].file.name;
    this.openFileStates[this.activeTab].file.name = name;
    this.fileStates.forEach((state, index) => {
      if (state.file.name == oldName) {
        this.fileStates[index].file.name = name;
        return;
      }
    });
    this.openFileStates[this.activeTab].unsaved = true;
  }

  private handleLintSwitcher(): void {
    if (this.lintData.status == "done") {
      this.showLint = !this.showLint;
    } else if (
      this.lintData.status == "processing" &&
      this.remainingLintChecks <= 0
    ) {
      this.remainingLintChecks = 3;
      this.lintCheckTimer = setInterval(this.handleLintTimer, 1000);
    }
  }

  private async loadProject(event: FileEvent): Promise<void> {
    //get files from user file event and show it in UI
    if (event.files.length == 0) {
      this.openFileStates = [
        {
          edited: false,
          unsaved: false,
          file: { name: "unnamed", path: "unnamed", content: "" },
        },
      ];
    } else {
      this.fileStates = [];
      for (let file of event.files) {
        this.fileStates.push({ edited: false, unsaved: false, file: file });
      }
      this.fileIdCounter = 0;
      this.openFileStates = this.fileStates.slice();
      //generate unique ID for the v-for :key directive
      this.openFileStates.forEach((state, index) => {
        this.openFileStates[index].id = this.fileIdCounter;
        this.fileIdCounter++;
      });

      //upload files to backend
      this.uploading = true;
      //extract file handles from file states
      let fileHandles: FileHandle[] = [];
      for (const fileState of this.fileStates) {
        fileHandles.push(fileState.file);
      }
      if (this.projectData.language == "auto") {
        //TODO right now the whole project's language is being read from the first file. this is not great but I don't really know what else to do.
        this.detectedLanguage = getLanguage(fileHandles[0].name);
      }
      let result = await API.submitProject({
        name: event.projectName,
        files: fileHandles,
        language: this.detectedLanguage,
        linter: this.projectData.linter,
      });
      if (result.errorMessage != undefined) {
        console.log(result.errorMessage);
        this.uploading = false;
        this.fileStates = [
          {
            edited: false,
            unsaved: false,
            file: { name: "unnamed", path: "unnamed", content: "" },
          },
        ];
        this.openFileStates = this.fileStates.slice();
        this.showUploader = true;
        this.$emit("notification", {
          type: "error",
          message: result.errorMessage,
        });
        return;
      }
      this.showUploader = false;
      this.projectData.data = result;
      this.uploading = false;
      this.$emit("new-project", {
        settings: this.projectData,
        files: this.fileStates,
      });

      //set interval for asking for lint status every second. handler has to deactivate asking for lint results on receiving results (or an error)
      this.lintData.status = "processing";
      this.lintCheckTimer = setInterval(this.handleLintTimer, 1000);
    }
  }

  private convertLintFilesToDict(): void {
    for (const lintFile of this.lintData.lintFiles) {
      this.lintsByFile[lintFile.name] = lintFile.lints;
    }
  }

  private async handleLintTimer() {
    if (this.remainingLintChecks > 0) {
      this.remainingLintChecks--;
      this.lintData = await API.getLint(this.projectData.data.projectId); //TODO proper project handling. Should use ID instead?
      console.log("lintData", this.lintData.lintFiles);

      if (this.lintData.status != "processing") {
        clearInterval(this.lintCheckTimer);
        if (this.lintData.status == "done") {
          this.convertLintFilesToDict();
        } else {
          this.$emit("notification", {
            type: "error",
            message: this.lintData.errorMessage,
          });
        }
      }
    } else {
      clearInterval(this.lintCheckTimer);
      this.$emit("notification", {
        type: "info",
        message:
          "Fetching lint results timed out. Server may still be processing, you can retry.",
      });
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
