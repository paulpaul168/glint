<template>
  <v-item-group>
    <v-row>
      <v-col class="lint-header-col" cols="9">
        <v-card-title class="lint-header">{{ lint.header }}</v-card-title>
      </v-col>
      <v-col class="lint-header-col text-right" style="padding-right: 0">
        <v-tooltip bottom open-delay="1000">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              text
              small
              elevation="0"
              class="lint-file-btn"
              v-bind="attrs"
              v-on="on"
              @click="goToFile"
            >
              {{ fileLinkText }}
            </v-btn>
          </template>
          <span>Jump to location</span>
        </v-tooltip>
        <!--<a target="_blank" :href="lint.fileName" class="lint-url">
          {{ fileLinkText }}
        </a>-->
      </v-col>
    </v-row>
    <v-row>
      <v-card outlined elevation="2" class="lint-snippet rounded-md">
        <v-card-text
          class="lint-text"
          style="background-color: var(--v-bg_tertiary-base)"
        >
          {{ lint.message }}
        </v-card-text>
        <v-divider></v-divider>
        <code-view
          :lineNumbers="false"
          :readonly="true"
          :fileState="internalFileState"
          :height="'auto'"
          :language="'auto'"
        ></code-view>
      </v-card>
    </v-row>
    <v-row dense v-if="lint.url">
      <a target="_blank" :href="lint.url" class="lint-url">{{ lint.url }}</a>
    </v-row>
  </v-item-group>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import CodeView from "@/components/CodeView.vue";
import { FileState, Lint } from "./types/interfaces";

@Component({
  components: {
    CodeView,
  },
})
export default class LintCard extends Vue {
  name = "LintCard";
  @Prop() lint!: Lint;
  @Prop() fileState!: FileState;

  private snippetStartLine = 0;
  private snippetEndLine = 0;
  private internalFileState: FileState = {
    file: { name: "unnamed", path: "unnamed", content: "" },
    language: "auto",
    detectedLanguage: "txt",
    unsaved: false,
    edited: false,
  };
  private fileLinkText = "";

  created(): void {
    this.lintChanged();
  }

  @Watch("fileState") //does this really work like this?
  @Watch("lint")
  private lintChanged(): void {
    let codeSnippet = "";
    this.snippetStartLine = this.lint.line - 1;
    if (this.lint.endLine == null || this.lint.endLine <= this.lint.line) {
      this.snippetEndLine = this.lint.line;
    } else {
      this.snippetEndLine = this.lint.endLine;
    }
    codeSnippet = this.fileState.file.content
      .split("\n")
      .slice(this.snippetStartLine, this.snippetEndLine)
      .join("\n");
    this.internalFileState.file.name = this.fileState.file.name;
    this.internalFileState.language = this.fileState.language;
    this.internalFileState.detectedLanguage = this.fileState.detectedLanguage;
    this.internalFileState.file.content = codeSnippet;
    if (this.snippetEndLine - this.snippetStartLine > 1) {
      this.fileLinkText =
        "lines " + this.snippetStartLine + "-" + this.snippetEndLine;
    } else {
      this.fileLinkText = "line " + this.snippetStartLine;
    }
  }

  private goToFile(): void {
    this.$emit("go-to-source", {
      filePath: this.internalFileState.file.path,
      line: this.snippetStartLine,
    });
  }
}
</script>

<style scoped>
.lint-header {
  margin-top: 1em;
  padding-left: 0;
  padding-bottom: 0em;
  text-align: left;
}

.lint-snippet {
  width: 100%;
  margin-bottom: 1em;
  margin-right: 1em;
}

.lint-text {
  text-align: left;
  padding: 0.7em;
}

.lint-url {
  padding: 0.6em;
  padding-top: 0em;
  text-decoration: none;
  transition: 0.1s;
}

.lint-url:hover {
  transition: 0.2s;
  color: var(--v-accent-base);
}

.lint-header-col {
  height: auto;
  margin-top: auto;
  margin-bottom: 0;
  padding-bottom: 0.2em;
}

.lint-file-btn {
  margin-right: 1.3em;
  text-transform: none;
  color: var(--v-primary-base);
  transition: 0.1s;
}

.lint-file-btn:hover {
  text-transform: none;
  color: var(--v-accent-base);
  transition: 0.2s;
}
</style>
