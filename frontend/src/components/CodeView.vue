<template>
  <prism-editor
    class="code-editor"
    v-model="internalState.file.content"
    :highlight="highlighter"
    :line-numbers="lineNumbers == true"
    :readonly="readonly == true"
    @input="codeEdited"
  >
  </prism-editor>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import { FileState } from "./types/interfaces";

import { PrismEditor } from "vue-prism-editor";
import "vue-prism-editor/dist/prismeditor.min.css";

import { highlight, languages } from "prismjs";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-python";
import "prismjs/components/prism-markdown";
import "prismjs/themes/prism-tomorrow.css";

@Component({
  components: {
    PrismEditor,
  },
})
export default class CodeView extends Vue {
  name = "CodeView";

  @Prop({ default: false }) readonly!: boolean;
  @Prop({ default: true }) lineNumbers!: boolean;
  @Prop({
    default: () => ({
      file: { name: "unnamed", path: "unnamed", content: "" },
      unsaved: false,
      edited: false,
    }),
  })
  fileState!: FileState;

  private internalState: FileState = {
    file: { name: "unnamed", path: "unnamed", content: "" },
    unsaved: false,
    edited: false,
  };

  created(): void {
    this.internalState = this.fileState;
  }

  @Watch("fileState")
  fileStateChanged(newState: FileState): void {
    this.internalState.file = newState.file; //TODO not sure if I should copy the other parameters as well (= entire object). depends on what the state changed would even be used for, right now it'll just never happen.
    console.log("state changed", this.internalState.file.name);
  }

  private codeEdited(): void {
    this.internalState.edited = true;
    this.internalState.unsaved = true;
    this.$emit("input", this.internalState);
  }

  highlighter(code: string): string {
    let extension = this.internalState.file.name.split(".").pop(); //TODO: on tab switch this is apparently called again for each tab and then the highlight language is incorrect because active tab is incorrect. investigate
    let language = "";
    switch (extension) {
      case "py":
        language = "python";
        break;
      case "ts":
      case "js":
        language = "javascript";
        break;
      case "vue":
        language = "html";
        break;
      case "md":
        language = "markdown";
        break;
      default:
        console.log("Couldn't find a language to apply for highlighting");
        return code;
    }
    return highlight(code, languages[language], language);
  }
}
</script>

<style scoped>
.code-editor {
  background: var(--bg_primary);
  color: var(--primary);

  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 15px;
  line-height: 1.5;
  padding: 5px;

  height: auto;
}
</style>
