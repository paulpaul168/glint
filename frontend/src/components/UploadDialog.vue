<template>
  <v-card v-if="show">
    <v-card-title>Upload File</v-card-title>
    <v-card-text></v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="secondary" @click="close">Cancel</v-btn>
      <v-btn color="primary">Upload</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import * as API from "../services/BackendAPI";

@Component
export default class UploadDialog extends Vue {
  @Prop() private show!: boolean;
  private name = "UploadDialog";

  close(): void {
    this.show = false;
  }

  async upload(): Promise<boolean> {
    return false;
  }
}
</script>
