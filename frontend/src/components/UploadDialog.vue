<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        class="rounded-sm"
        v-bind="attrs"
        v-on="on"
        @drop.prevent="dropFile"
        @dragover.prevent
      >
        <v-icon large>mdi-upload</v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-title>Upload File</v-card-title>
      <v-card-text>
        <v-file-input
          class="rounded-sm"
          accept="text/*"
          label="Select one or more files to upload or .zip of project"
          multiple
          show-size
          prepend-icon="mdi-file-code"
          @change="selectFiles"
          @drop.prevent="dropFile(files)"
          @dragover.prevent
        ></v-file-input>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="secondary" @click="close">Cancel</v-btn>
        <v-btn color="primary" @click="upload">Upload</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import * as API from "../services/BackendAPI";
import { FileHandle, FileEvent } from "./types/upload-dialog-types";

@Component
export default class UploadDialog extends Vue {
  private name = "UploadDialog";
  private dialog = false;
  private selectedFiles: FileHandle[] = [];
  private selectedFile!: File;

  private close(): void {
    this.selectedFiles = [];
    this.dialog = false;
  }

  private dropFile(files: File): void {
    console.log("dropped file", files);
  }

  private async selectFiles(files: File[]): Promise<void> {
    for (let file of files) {
      this.selectedFiles.push({ name: file.name, content: await file.text() });
    }
  }

  private async upload(): Promise<boolean> {
    let upFiles: FileHandle[];
    let event: FileEvent;
    upFiles = [
      { name: "hello", content: "world" },
      { name: "hello2", content: "world2" },
    ];
    event = { files: this.selectedFiles };
    this.$emit("file-event", event);
    return true;
  }
}
</script>
