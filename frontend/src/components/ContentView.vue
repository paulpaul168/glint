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

            <v-tooltip bottom open-delay="1000" v-if="hasLint">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  small
                  elevation="0"
                  color="transparent"
                  v-bind="attrs"
                  v-on="on"
                  @click="showLint = !showLint"
                >
                  <v-icon small v-if="showLint">mdi-pencil</v-icon>
                  <v-icon small v-else>mdi-format-list-bulleted</v-icon>
                </v-btn>
              </template>
              <span v-if="showLint">Show Source</span>
              <span v-else>Show Lint</span>
            </v-tooltip>
          </v-toolbar>
          <lint-view v-if="showLint"></lint-view>
          <code-view v-bind:fileState="state" v-else></code-view>
          <upload-dialog
            class="file-uploader"
            v-if="!showFile"
            @file-event="loadFiles($event)"
          ></upload-dialog>
        </v-tab-item>
      </v-tabs-items>
    </v-row>
  </v-item-group>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import UploadDialog from "@/components/UploadDialog.vue";
import CodeView from "@/components/CodeView.vue";
import LintView from "@/components/LintView.vue";

import { FileEvent, FileState } from "./types/upload-dialog-types";

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
  private hasLint = false;
  private activeTab = 0;
  private fileStates: FileState[] = [
    {
      edited: false,
      unsaved: false,
      file: { name: "unnamed", path: "unnamed", content: "" },
    },
  ];

  codeEdited(): void {
    if (this.showFile == false) {
      this.showFile = true; //TODO probably more to do here once that happens (someone writing in an empty file while the upload button is showing)
    }
    this.fileStates[this.activeTab].edited = true;
    this.fileStates[this.activeTab].unsaved = true;
  }

  loadFiles(event: FileEvent): void {
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
      this.hasLint = true;
    }
  }
}
</script>

<style scoped>
.main-pane {
  border: #1e1e1e solid 0 !important;
  border-bottom-right-radius: 5px !important;
}

.file-tabs {
  background-color: var(--v-bg_tertiary-base);
  border: #1e1e1e solid 0px;
  border-top-right-radius: 5px !important;
}

.main-file-view {
  width: 100%;
}

.toolbar {
  position: absolute;
  width: 100%;
  z-index: 10;
}
</style>
