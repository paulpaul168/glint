<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        class="rounded-md dialog-button"
        elevation="0"
        v-bind="attrs"
        v-on="on"
        @drop.prevent="dropFile"
        @dragover.prevent
      >
        <v-icon x-large>mdi-plus</v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-title>Upload File</v-card-title>
      <v-card-text>
        <v-text-field
          label="Enter Project Name"
          v-model="projectName"
        ></v-text-field>
        <v-file-input
          class="rounded-md"
          accept="text/*"
          label="Select one or more files to upload or .zip of project"
          multiple
          show-size
          prepend-icon="mdi-file-code"
          @change="selectFiles"
          @drop="dropFile(files)"
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
import { Component, Vue } from "vue-property-decorator";
import * as API from "../services/BackendAPI";
import { FileHandle, FileEvent } from "./types/interfaces";

@Component
export default class UploadDialog extends Vue {
  private name = "UploadDialog";
  private dialog = false;
  private projectName = "";
  private selectedFiles: FileHandle[] = [];

  private close(): void {
    this.selectedFiles = [];
    this.dialog = false;
  }

  private async dropFile(event: DragEvent): Promise<void> {
    if (event.dataTransfer != null) {
      await this.selectFiles(Array.from(event.dataTransfer.files));
      this.upload();
      //this.selectFiles(event.dataTransfer.files);
    }
    //console.log("dropped files", event.dataTransfer.files);
  }

  private async selectFiles(files: File[]): Promise<void> {
    this.selectedFiles = [];
    for (let file of files) {
      this.selectedFiles.push({
        name: file.name,
        path: file.name, //TODO needs to be extended once .zip is supported
        content: await file.text(),
      });
    }
  }

  private async upload(): Promise<boolean> {
    let event: FileEvent = { files: this.selectedFiles };
    this.$emit("file-event", event);
    let result = await API.submitProject(this.projectName, this.selectedFiles); //add language detection here. best to move the language detection to a separate .ts and call it in fileview for highlighting and here for sending to backend. language detection per file and for now just take eg: first file in list for detection here
    console.log("result", result);
    this.dialog = false;
    //TODO return the result (maybe somehow reformatted) here to allow for proper project management in the side pane. can't do right now because data structure with interfaces and all still has to be designed/planned.
    return true;
  }
}
</script>

<style scoped>
.dialog-button {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -100%);
  padding: 6% !important;
}
</style>
