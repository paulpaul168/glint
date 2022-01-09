<template>
  <div class="d-flex flex-row file">
    <v-btn
      :class="'file-name text-body-1 ' + (isClickable ? '' : 'disable-button')"
      text
      :ripple="false"
      @click="clickFile"
    >
      {{ state.file.name }}
    </v-btn>
    <v-spacer></v-spacer>
    <v-btn v-if="active" class="delete-mapping-button" icon @click="deleteFile">
      <v-icon color="#cccccc" small>mdi-delete</v-icon>
    </v-btn>
    <span v-if="nrWarnings" style="margin: auto 0.2em; color: grey">
      {{ nrWarnings }}
    </span>
    <v-icon v-if="nrWarnings" color="warning" small>mdi-alert-circle</v-icon>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { FileState, Project } from "../types/interfaces";

@Component({
  components: {},
})
export default class File extends Vue {
  name = "File";
  @Prop() project!: Project;
  @Prop({ default: "" }) folderTree!: string;
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

  private nrWarnings = 0;

  @Watch("project.lintData", { immediate: true })
  lintsChange(): void {
    for (const lintFile of this.project.lintData.lintFiles) {
      if (lintFile.path == this.folderTree + this.state.file.path) {
        this.nrWarnings = lintFile.lints.length;
        return;
      }
    }
    this.nrWarnings = 0;
  }

  private clickFile(): void {
    this.$emit("open-file", {
      filePath: this.state.file.path,
      projectId: this.project.settings.data.projectId,
    });
  }

  private deleteFile(): void {
    this.$emit("delete-file", {
      filePath: this.state.file.path,
      projectId: this.project.settings.data.projectId,
    });
  }
}
</script>

<style scoped>
.file {
  margin: 0 0.4em;
  width: auto;
}

.file-name {
  text-transform: none;
  justify-content: left;
  padding-left: 4px !important;
  padding-right: 8px !important; /*TODO: I'd like to have this auto expand to use the remaining space */
  flex-grow: 100;
  margin-right: 0.2em;
}

.file-name::v-deep .v-btn__content {
  overflow: hidden;
  white-space: nowrap;
  max-width: 300px;
  text-overflow: ellipsis;
  display: inline-block;
  text-align: left;
}

.disable-button {
  pointer-events: none;
}
</style>
