<template>
  <prism-editor
    :style="'height: ' + height"
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
import "prismjs/components/prism-typescript";
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
  @Prop({ default: "calc(100% - 26px)" }) height!: string;
  @Prop({
    default: () => ({
      language: "auto",
      detectedLanguage: "auto",
      file: { name: "unnamed", path: "unnamed", content: "" },
      unsaved: false,
      edited: false,
    }),
  })
  private fileState!: FileState;

  private internalState: FileState = {
    language: "auto",
    detectedLanguage: "auto",
    file: { name: "unnamed", path: "unnamed", content: "" },
    unsaved: false,
    edited: false,
  };

  created(): void {
    this.fileStateChanged();
  }

  @Watch("fileState")
  fileStateChanged(): void {
    this.internalState = this.fileState;
    this.highlighter(this.internalState.file.content);
  }

  private codeEdited(): void {
    this.internalState.edited = true;
    this.internalState.unsaved = true;
    this.$emit("input", this.internalState);
  }

  highlighter(code: string): string {
    let highlightLanguage = this.internalState.language;
    if (highlightLanguage == "auto") {
      highlightLanguage = this.internalState.detectedLanguage;
    }
    //TODO: on tab switch this is apparently called again for each tab and then the highlight language is incorrect because active tab is incorrect. investigate
    if (highlightLanguage == "txt") {
      return code;
    }
    return highlight(code, languages[highlightLanguage], highlightLanguage);
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

  overflow-y: auto !important;

  scrollbar-color: var(--v-bg_tertiary-base) var(--v-bg_secondary-base);
  border-bottom-right-radius: 50px;
}
</style>
