<template>
  <v-item-group>
    <v-row>
      <v-tabs>
        <v-tab v-for="file in files" :key="file.name">{{ file.name }}</v-tab>
      </v-tabs>
    </v-row>
    <v-row justify="center">
      <prism-editor
        v-if="showFile"
        class="code-editor"
        v-model="activeFileContent"
        :highlight="highlighter"
        line-numbers
      ></prism-editor>
      <upload-dialog v-else @file-event="loadFiles($event)"></upload-dialog>
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
import "prismjs/themes/prism-tomorrow.css";

import UploadDialog from "@/components/UploadDialog.vue";

import { FileEvent } from "./types/upload-dialog-types";

@Component({
  components: {
    PrismEditor,
    UploadDialog,
  },
})
export default class FileView extends Vue {
  private name = "FileView";
  private activeFileContent = "";
  private code = "def abc(def):\n  x = y + 4";
  private showFile = false;
  private showDialog = false;
  private files: FileEvent["files"] = [{ name: "unnamed", content: "" }];

  highlighter(code: string): string {
    return highlight(code, languages.python, "");
  }

  loadFiles(event: FileEvent): void {
    this.files = event.files;
    this.activeFileContent = this.files[0].content;
    this.showFile = true;
  }
}
</script>

<style scoped>
.code-editor {
  background: var(--bg_primary);
  color: var(--primary);

  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 15px;
  line-height: 1.5;
  padding: 5px;
}
</style>
