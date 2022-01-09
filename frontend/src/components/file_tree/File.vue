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
    <v-btn
      v-if="active"
      class="delete-mapping-button"
      icon
      @click="
        $emit('delete-file', {
          filePath: state.file.path,
          projectId: project.settings.data.projectId,
        })
      "
    >
      <v-icon small>mdi-delete</v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { FileState, Project } from "../types/interfaces";

@Component({
  components: {},
})
export default class File extends Vue {
  name = "File";
  @Prop() project!: Project;
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
    this.$emit("open-file", {
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
  flex-grow: 1;
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
