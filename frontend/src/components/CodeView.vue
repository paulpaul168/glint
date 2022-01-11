<template>
  <prism-editor
    :id="id"
    ref="editor"
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
import "prismjs/components/prism-markup-templating";
import "prismjs/components/prism-php";
import "prismjs/components/prism-go";
import "prismjs/components/prism-rust";
import "prismjs/components/prism-markdown";
import "prismjs/themes/prism-tomorrow.css";

@Component({
  components: {
    PrismEditor,
  },
})
export default class CodeView extends Vue {
  name = "CodeView";

  @Prop({ default: "" }) id!: string;
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

  scrollToLine(line: number): void {
    const editor = document.getElementById("prismeditor");
    const editorContainer = (
      editor?.getElementsByClassName(
        "prism-editor__container"
      ) as HTMLCollection
    )[0];
    const editorContent = editorContainer.childNodes[1].childNodes;
    let lineCounter = 0;
    let reachedLine = false;
    let lastElementNode: HTMLElement;
    //let focusElement; //I can't do anything with the actual focus element as that's a
    //text node and I can't scroll to a text node. I'll keep this in, in case I find a way
    //to utilise this in the future (highlighting?)
    for (const child of editorContent) {
      if (child.nodeType == 1) {
        lastElementNode = child as HTMLElement;
        console.log("last element");
      }
      if (child.nodeValue != null) {
        let pos = child.nodeValue.indexOf("\n");
        while (pos != -1) {
          lineCounter++;
          if (lineCounter >= line) {
            reachedLine = true;
            break;
          }
          pos = child.nodeValue.indexOf("\n", pos + 1);
        }
        if (reachedLine) {
          //focusElement = child;
          break;
        }
      }
    }

    if (editor != undefined) {
      this.$nextTick(() => {
        console.log("scrolling to lastElement", lastElementNode);
        editor.scrollTo(0, (lastElementNode as HTMLElement).offsetTop);
      });
    }
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

  font-family: "Fira code", "Fira Mono", "Consolas", "Menlo", "Courier New",
    monospace;
  font-size: 15px;
  line-height: 1.5;
  padding: 5px;

  overflow-y: auto !important;

  scrollbar-color: var(--v-bg_tertiary-lighten1) var(--v-bg_secondary-base);
  border-bottom-right-radius: 5px;
}
</style>
