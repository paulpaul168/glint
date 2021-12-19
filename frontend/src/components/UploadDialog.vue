<template>
  <v-dialog v-model="dialog" max-width="600">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        :class="'rounded-md dialog-button ' + dragClass"
        elevation="0"
        :loading="uploading"
        v-bind="attrs"
        v-on="on"
        @dragover.prevent="dialogDrag = true"
        @dragleave="dialogDrag = false"
        @drop.prevent="dropFile"
      >
        <!--<v-icon x-large v-if="dialogDrag">
          mdi-clipboard-arrow-down-outline
        </v-icon>-->
        <v-icon x-large :class="dragIconClass">mdi-plus</v-icon>
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
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { FileHandle, FileEvent } from "./types/interfaces";

@Component
export default class UploadDialog extends Vue {
  private name = "UploadDialog";
  @Prop({ default: false }) uploading!: boolean;

  private dialog = false;
  private dialogDrag = false;
  private dragIconClass = "";
  private dragClass = "";
  private projectName = "";
  private selectedFiles: FileHandle[] = [];

  @Watch("dialogDrag")
  private dragChange() {
    if (this.dialogDrag) {
      this.dragClass = "dialog-button-drag";
      this.dragIconClass = "dialog-icon-drag";
    } else {
      this.dragClass = "";
      this.dragIconClass = "";
    }
  }

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

  private upload(): void {
    let event: FileEvent = {
      projectName: this.projectName,
      files: this.selectedFiles,
    };
    this.$emit("file-event", event);
    this.dialog = false;
    //TODO return the result (maybe somehow reformatted) here to allow for proper project management in the side pane. can't do right now because data structure with interfaces and all still has to be designed/planned.
    return;
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

.dialog-button-drag {
  background-color: #383838 !important;
  transition: background-color 0.2s cubic-bezier(0.4, 0, 0.6, 1);
}

.dialog-icon-drag {
  transform: scale(1.2);
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.6, 1);
}
</style>
