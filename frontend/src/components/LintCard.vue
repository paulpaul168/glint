<template>
  <v-item-group>
    <v-row>
      <v-card-title class="lint-header">{{ lint.header }}</v-card-title>
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
    unsaved: false,
    edited: false,
  };

  created(): void {
    this.lintChanged();
  }

  @Watch("fileState") //does this really work like this?
  @Watch("lint")
  private lintChanged(): void {
    let codeSnippet = "";
    this.snippetStartLine = this.lint.line;
    this.snippetEndLine = this.lint.endLine;
    codeSnippet = this.fileState.file.content
      .split("\n")
      .slice(this.snippetStartLine, this.snippetEndLine)
      .join("\n");
    this.internalFileState.file.name = this.fileState.file.name;
    this.internalFileState.file.content = codeSnippet;
  }
}
</script>

<style scoped>
.lint-header {
  margin-top: 1em;
  padding-bottom: 0.2em;
}

.lint-snippet {
  width: 98%;
  margin-bottom: 1em;
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
  text-decoration: underline;
}
</style>
