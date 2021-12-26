<template>
  <v-container class="lint-view">
    <div style="height: 100%" v-if="lints.length == 0">
      <h2 style="position: relative; top: 45%">No Lint results found</h2>
    </div>
    <ul
      v-for="lint in lints"
      :key="lint.line + '_' + lint.column + '_' + lint.header"
    >
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
    default: () => [],
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

.code-editor {
  height: auto !important;
}
</style>
