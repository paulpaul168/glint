<template>
  <v-dialog v-model="dialog" max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        class="rounded-md dialog-button"
        color="primary"
        text
        elevation="0"
        :loading="uploading"
        v-bind="attrs"
        v-on="on"
      >
        <v-icon left small>mdi-plus</v-icon>File
      </v-btn>
    </template>

    <v-card>
      <v-card-title>Upload File</v-card-title>
      <v-card-text>
        <v-text-field
          label="Enter File Path (optional)"
          v-model="filePath"
        ></v-text-field>
        <v-file-input
          class="rounded-md"
          accept="text/*"
          label="Select one or more files to upload"
          multiple
          show-size
          prepend-icon="mdi-file-code"
          @change="selectFiles"
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
import { getLanguage } from "@/services/LanguageDetection";
import { Component, Prop, Vue } from "vue-property-decorator";
import { AddFileEvent, FileState } from "./types/interfaces";

@Component
export default class UploadFileDialog extends Vue {
  name = "UploadFileDialog";
  @Prop({ default: "" }) projectId!: string;
  @Prop({ default: false }) uploading!: boolean;

  private dialog = false;
  private filePath = "";
  private selectedFiles: FileState[] = [];

  private close(): void {
    this.selectedFiles = [];
    this.dialog = false;
  }

  private async selectFiles(files: File[]): Promise<void> {
    this.selectedFiles = [];
    let sanitizedFilePath = this.filePath;
    //there has to be a better and more robust way to sanitize file paths
    if (sanitizedFilePath.charAt(0) == "/") {
      sanitizedFilePath = sanitizedFilePath.substring(1);
    }
    if (
      sanitizedFilePath.length > 0 &&
      sanitizedFilePath.charAt(sanitizedFilePath.length - 1) != "/"
    ) {
      sanitizedFilePath += "/";
    }
    for (let file of files) {
      this.selectedFiles.push({
        file: {
          name: file.name,
          path: sanitizedFilePath + file.name,
          content: await file.text(),
        },
        language: "auto",
        detectedLanguage: getLanguage(file.name),
        unsaved: false,
        edited: false,
      });
    }
  }

  private upload(): void {
    const eventData: AddFileEvent = {
      projectId: this.projectId,
      files: this.selectedFiles,
    };
    this.$emit("upload-files", eventData);
    this.dialog = false;
    return;
  }
}
</script>

<style scoped>
.dialog-button {
  margin: 0.6em;
  margin-bottom: 0;
  text-transform: none;
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
