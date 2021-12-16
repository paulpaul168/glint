<template>
  <v-container class="lint-view">
    <ul v-for="lint in lints" :key="lint.line">
      <lint-card :lint="lint" :fileState="fileState"></lint-card>
    </ul>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { FileState, Lint } from "./types/interfaces";

import LintCard from "@/components/LintCard.vue";

@Component({
  components: {
    LintCard,
  },
})
export default class LintView extends Vue {
  name = "LintView";
  @Prop({
    default: () => [
      {
        fileName: "BackendAPI.ts",
        line: 1,
        endLine: 2,
        column: 15,
        endColumn: 35,
        header: "Header msg",
        message: "Long msg body with a lot of information and text!",
        url: "https://domain.com/some_cool_url",
      },
      {
        fileName: "BackendAPI.ts",
        line: 7,
        endLine: 10,
        column: 10,
        endColumn: 15,
        header: "Header msg 2",
        message:
          "Even longer msg body with even more information and a lot more text. Wow!",
      },
      {
        fileName: "BackendAPI.ts",
        line: 15,
        endLine: 20,
        column: 15,
        endColumn: 35,
        header: "What a wild header message",
        message: "Wow! This is so cool! The design is decent and I think it's also fairly usable. Now let's see how it looks like when there's a *really* long text, just to make sure that on stupidly long error messages the styling still works out alright",
        url: "https://domain.com/some_other_but_longer_cool_url/hello",
      },
      {
        fileName: "BackendAPI.ts",
        line: 38,
        endLine: 40,
        column: 10,
        endColumn: 15,
        header: "No msg header",
        message: "",
        url: "https://domain.com/last_url",
      },
      {
        fileName: "BackendAPI.ts",
        line: 25,
        endLine: 26,
        column: 10,
        endColumn: 15,
        header: "Filler 1",
        message: "This is a filler element",
        url: "https://domain.com/filler_url",
      },
      {
        fileName: "BackendAPI.ts",
        line: 26,
        endLine: 28,
        column: 10,
        endColumn: 15,
        header: "Filler 2",
        message: "This is a filler element",
        url: "https://domain.com/filler_url",
      },
      {
        fileName: "BackendAPI.ts",
        line: 28,
        endLine: 30,
        column: 10,
        endColumn: 15,
        header: "Filler 3",
        message: "This is a filler element",
        url: "https://domain.com/filler_url",
      },
    ],
  })
  lints!: Lint[];
  @Prop({
    default: () => ({
      file: { name: "unnamed", path: "unnamed", content: "" },
      unsaved: false,
      edited: false,
    }),
  })
  fileState!: FileState;
}
</script>

<style scoped>
.lint-view {
  border: var(--v-bg_secondary-base) solid 0 !important;
  border-bottom-right-radius: 5px !important;

  height: 100%;
  overflow-y: auto !important;

  scrollbar-color: var(--v-bg_tertiary-base) var(--v-bg_secondary-base);
  border-bottom-right-radius: 50px;
}
</style>
