<template>
  <v-item-group>
    <v-row>
      <v-tabs
        v-model="activeTab"
        show-arrows
        class="file-tabs"
        background-color="bg_tertiary"
      >
        <v-tab v-for="state in fileStates" :key="state.file.name">
          {{ state.file.name }}<p v-if="state.unsaved">*</p>
        </v-tab>
        <!--<v-tab v-if="showFile">
          <v-icon>mdi-plus</v-icon>
        </v-tab>-->
      </v-tabs>
    </v-row>
    <v-row>
      <v-tabs-items
        v-model="activeTab"
        class="main-file-view main-pane"
        justify="center"
        align="center"
      >
        <v-tab-item v-for="state in fileStates" :key="state.file.name">
          <v-toolbar class="toolbar" dense elevation="0" color="transparent">
            <v-spacer></v-spacer>

            <v-tooltip bottom open-delay="1000" v-if="lintStatus">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  small
                  elevation="0"
                  color="transparent"
                  v-bind="attrs"
                  v-on="on"
                  :loading="lintStatus == 'processing'"
                  :disabled="lintStatus != 'done'"
                  @click="showLint = !showLint"
                >
                  <v-icon small v-if="showLint">mdi-pencil</v-icon>
                  <v-icon small v-else-if="!showLint && lintStatus == 'done'"
                    >mdi-format-list-bulleted</v-icon
                  >
                  <v-icon
                    small
                    v-else-if="
                      ((lintStatus != 'done') == lintStatus) != 'processing'
                    "
                    >mdi-alert-circle</v-icon
                  >
                </v-btn>
              </template>
              <span v-if="showLint">Show Source</span>
              <span v-else>Show Lint</span>
            </v-tooltip>
          </v-toolbar>
          <lint-view v-if="showLint" :fileState="state"></lint-view>
          <code-view v-else :fileState="state"></code-view>
          <upload-dialog
            v-if="!showFile"
            @file-event="loadFiles($event)"
          ></upload-dialog>
        </v-tab-item>
      </v-tabs-items>
    </v-row>
  </v-item-group>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";

import UploadDialog from "@/components/UploadDialog.vue";
import CodeView from "@/components/CodeView.vue";
import LintView from "@/components/LintView.vue";

import { FileEvent, FileState } from "./types/interfaces";

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
  private lintStatus = ""; //processing means lint is ongoing/result hasn't come in yet, done means lint has been received, anything else means error on linting
  private activeTab = 0;
  private fileStates: FileState[] = [
    {
      edited: false,
      unsaved: false,
      file: { name: "unnamed", path: "unnamed", content: "" },
    },
  ];

  @Watch("lintStatus")
  private updateLintToggle(): void {
    return;
  }

  private codeEdited(): void {
    if (this.showFile == false) {
      this.showFile = true; //TODO probably more to do here once that happens (someone writing in an empty file while the upload button is showing)
    }
    this.fileStates[this.activeTab].edited = true;
    this.fileStates[this.activeTab].unsaved = true;
  }

  private loadFiles(event: FileEvent): void {
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
      this.lintStatus = "done";
    }
  }
}
</script>

<style scoped>
.main-pane {
  border: var(--v-bg_secondary-base) solid 0 !important;
  border-bottom-right-radius: 5px !important;
}

.file-tabs {
  background-color: var(--v-bg_tertiary-base);
  border: var(--v-bg_secondary-base) solid 0px;
  border-top-right-radius: 5px !important;
}

.main-file-view {
  width: 100%;
  overflow-y: auto !important;
  height: calc(100vh - 130px);

  scrollbar-color: var(--v-bg_tertiary-base) var(--v-bg_secondary-base);
  border-bottom-right-radius: 50px;
}

.toolbar {
  position: absolute;
  width: 100%;
  z-index: 10;
}
</style>
