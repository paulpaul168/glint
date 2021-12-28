<template>
  <div>{{ state.file.name }}</div>
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
}
</script>

<style scoped>

</style>
