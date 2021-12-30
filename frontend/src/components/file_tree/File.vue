<template>
  <div style="margin: 0 0.4em" class="d-flex flex-row">
    <v-btn
      :class="'file-name text-body-1 ' + (isClickable ? '' : 'disable-button')"
      text
      :ripple="false"
      @click="clickFile"
    >
      {{ state.file.name }}
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { FileState } from "../types/interfaces";

@Component({
  components: {},
})
export default class File extends Vue {
  name = "File";
  @Prop({ default: false }) active!: boolean;
  @Prop({ default: true }) isClickable!: boolean;
  @Prop({
    default: {
      language: "auto",
      detectedLanguage: "txt",
      unsaved: false,
      edited: false,
      file: {
        name: "<file name>",
        path: "<path>",
        content: "",
      },
    },
  })
  state!: FileState;

  private clickFile(): void {
    console.log("clicked file");
  }
}
</script>

<style scoped>
.file-name {
  text-transform: none;
  justify-content: left;
  padding-left: 4px !important;
  padding-right: auto !important;
  flex-grow: 1;
}

.disable-button {
  pointer-events: none;
}
</style>
