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
          style="text-transform: none"
          v-for="state in fileStates"
          :key="state.file.name"
        >
          {{ state.file.name }}<p v-if="state.unsaved">*</p>
        </v-tab>
        <!--<v-tab v-if="showFile">
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
          v-for="state in fileStates"
          :key="state.file.name"
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
          <lint-view v-if="showLint" :fileState="state"></lint-view>
          <code-view
            v-else
            :fileState="state"
            :language="projectData.language"
          ></code-view>
          <upload-dialog
            v-if="!showFile"
            :uploading="uploading"
            @file-event="loadProject($event)"
          ></upload-dialog>
        </v-tab-item>
      </v-tabs-items>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import * as API from "@/services/BackendAPI";
import UploadDialog from "@/components/UploadDialog.vue";
import CodeView from "@/components/CodeView.vue";
import LintView from "@/components/LintView.vue";

import {
  FileEvent,
  FileHandle,
  FileState,
  LintEvent,
  ProjectData,
} from "./types/interfaces";

@Component({
  components: {
    UploadDialog,
    CodeView,
    LintView,
  },
})
export default class ContentView extends Vue {
  name = "ContentView";
  private showFile = false;
  private showLint = false;
  private lintCheckTimer!: number;
  private remainingLintChecks = 5;
  private projectData: ProjectData = {
    //the defaults here need to be removed at some point and synced with a separate @Prop projectdata
    name: "DefaultProject",
    id: "DefaultProject",
    language: "auto",
    linter: "auto",
    urls: {
      projectUrl: new URL(API.apiAddress), //I dislike these default, I'd love to not have to specify them at all, but I think I might need to because I need language defaults
      sourcesUrl: new URL(API.apiAddress),
      lintUrl: new URL(API.apiAddress),
    },
  };
  private lintData: LintEvent = {
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
  private activeTab = 0;
  private uploading = false;
  private fileStates: FileState[] = [
    {
      edited: false,
      unsaved: false,
      file: { name: "unnamed", path: "unnamed", content: "" },
    },
  ];

  private codeEdited(): void {
    if (this.showFile == false) {
      this.showFile = true; //TODO probably more to do here once that happens (someone writing in an empty file while the upload button is showing)
    }
    this.fileStates[this.activeTab].edited = true;
    this.fileStates[this.activeTab].unsaved = true;
  }

  private saveFile(): void {
    return;
  }

  private handleLintSwitcher(): void {
    if (this.lintData.status == "done") {
      this.showLint = !this.showLint;
    } else if (
      this.lintData.status == "processing" &&
      this.remainingLintChecks <= 0
    ) {
      this.remainingLintChecks = 3;
    }
  }

  private async loadProject(event: FileEvent): Promise<void> {
    //get files from user file event and show it in UI
    if (event.files.length == 0) {
      this.fileStates = [
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
      this.showFile = true;

      //upload files to backend
      this.uploading = true;
      let fileHandles: FileHandle[] = [];
      for (const fileState of this.fileStates) {
        fileHandles.push(fileState.file);
      }
      //console.log("reached get upload");
      let result = await API.submitProject(event.projectName, fileHandles); //add language detection here. best to move the language detection to a separate .ts and call it in fileview for highlighting and here for sending to backend. language detection per file and for now just take eg: first file in list for detection here
      console.log("result", result);
      //TODO better resilience against key errors (if some key is not contained in answer like on error)
      this.projectData.name = result["name"];
      this.projectData.id = result["projectId"];
      this.projectData.urls.projectUrl = new URL(result["projectUrl"]);
      this.projectData.urls.sourcesUrl = new URL(result["sourcesUrl"]);
      this.projectData.urls.lintUrl = new URL(result["lintUrl"]);
      this.uploading = false; //TODO later on I probably should look into error handling here + an event that uploading is finished to not hide the button instantly

      //set interval for asking for lint status every second. handler has to deactivate asking for lint results on receiving results (or an error)
      //console.log("reached get lint");
      this.lintData.status = "processing";
      this.lintCheckTimer = setInterval(this.handleLintTimer, 1000);
    }
  }

  private async handleLintTimer() {
    if (this.remainingLintChecks > 0) {
      this.remainingLintChecks--;
      let lintEvent = await API.getLint(this.projectData.name); //TODO proper project handling. Should use ID instead?
      this.lintData = lintEvent;

      if (this.lintData.status != "processing") {
        clearInterval(this.lintCheckTimer);
      }
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
