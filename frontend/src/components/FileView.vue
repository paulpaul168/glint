<template>
  <v-item-group>
    <v-row>
      <v-tabs>
        <v-tab>file1</v-tab>
        <v-tab>file2</v-tab>
      </v-tabs>
    </v-row>
    <v-row justify="center">
      <prism-editor
        v-if="showFile"
        class="code-editor"
        v-model="code"
        :highlight="highlighter"
        line-numbers
      ></prism-editor>
      <div v-else>
        <v-btn
          class=".rounded-sm"
          fab
          tile
          @click="openUploadDialog"
          @drop.prevent="dropFile"
          @dragover.prevent
        >
          <v-icon>file-upload</v-icon>
        </v-btn>
      </div>
      <upload-dialog :show="showDialog"></upload-dialog>
    </v-row>
  </v-item-group>
</template>

<script lang="ts">
import Vue from "vue";
import { PrismEditor } from "vue-prism-editor";
import "vue-prism-editor/dist/prismeditor.min.css";

import { highlight, languages } from "prismjs";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-python";
import "prismjs/themes/prism-tomorrow.css";

import UploadDialog from "@/components/UploadDialog.vue";

export default Vue.extend({
  name: "FileView",
  components: {
    PrismEditor,
    UploadDialog,
  },

  data: () => ({
    code: "def abc(def):\n  x = y + 4",
    showFile: false,
    showDialog: false,
  }),

  methods: {
    highlighter(code: string): string {
      return highlight(code, languages.python, "");
    },

    openUploadDialog(): void {
      this.showDialog = true;
    },

    dropFile(): void {
      console.log("dropped file");
      this.showFile = true;
    }
  },
});
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
