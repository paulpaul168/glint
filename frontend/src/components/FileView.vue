<template>
  <v-item-group>
    <v-row>
      <v-tabs v-model="activeTab" show-arrows>
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
        class="main-file-view"
        justify="center"
        align="center"
      >
        <v-tab-item v-for="state in fileStates" :key="state.file.name">
          <prism-editor
            class="code-editor"
            v-model="state.file.content"
            :highlight="highlighter"
            line-numbers
            @input="codeEdited"
          >
          </prism-editor>
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
import { PrismEditor } from "vue-prism-editor";
import "vue-prism-editor/dist/prismeditor.min.css";

import { highlight, languages } from "prismjs";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-python";
import "prismjs/components/prism-markdown";
import "prismjs/themes/prism-tomorrow.css";

import UploadDialog from "@/components/UploadDialog.vue";

import { FileEvent, FileHandle } from "./types/upload-dialog-types";

@Component({
  components: {
    PrismEditor,
    UploadDialog,
  },
})
export default class FileView extends Vue {
  private name = "FileView";
  private showFile = false;
  private activeTab = 0;
  private fileStates: {
    edited: boolean;
    unsaved: boolean;
    file: FileHandle;
  }[] = [
    {
      edited: false,
      unsaved: false,
      file: { name: "unnamed", path: "unnamed", content: "" },
    },
  ];

  codeEdited(): void {
    this.fileStates[this.activeTab].edited = true;
    this.fileStates[this.activeTab].unsaved = true;
  }

  highlighter(code: string): string {
    let extension = this.fileStates[this.activeTab].file.name.split(".").pop(); //TODO: on tab switch this is apparently called again for each tab and then the highlight language is incorrect because active tab is incorrect. investigate
    let language = "";
    switch (extension) {
      case "py":
        language = "python";
        break;
      case "ts":
      case "js":
        language = "javascript";
        break;
      case "vue":
        language = "html";
        break;
      case "md":
        language = "markdown";
        break;
      default:
        console.log("Couldn't find a language to apply for highlighting");
        return code;
    }
    return highlight(code, languages[language], language);
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
    }
  }
}
</script>

<style scoped>
.main-file-view {
  width: 100%;
}

.code-editor {
  background: var(--bg_primary);
  color: var(--primary);

  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 15px;
  line-height: 1.5;
  padding: 5px;

  overflow-y: auto !important;
  height: calc(100vh - 135px);
}
</style>
