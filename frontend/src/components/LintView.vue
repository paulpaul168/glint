<template>
  <v-container class="lint-view">
    <div style="height: 100%" v-if="lints.length == 0">
      <h2 style="position: relative; top: 45%">
        <div
          v-if="
            availableLinterMappings[
              getLanguagePassthrough(fileState.file.name)
            ] == undefined
              ? false
              : availableLinterMappings[
                  getLanguagePassthrough(fileState.file.name)
                ].length > 0
          "
        >
          <span>{{ linter }}</span>
          <span style="color: grey">
            found no relevant problems in this file.
          </span>
        </div>
        <div v-else>
          <span style="color: grey">
            No linters available for this source file language.
          </span>
        </div>
      </h2>
    </div>
    <v-alert :value="outdated" class="outdated-notif" dense type="warning">
      Lint is outdated. Request new lint to get result fitting to new code.
    </v-alert>
    <ul
      v-for="lint in lints"
      :key="lint.line + '_' + lint.column + '_' + lint.header"
    >
      <lint-card
        :lint="lint"
        :fileState="fileState"
        v-on="$listeners"
      ></lint-card>
    </ul>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { FileState, Lint } from "./types/interfaces";

import LintCard from "@/components/LintCard.vue";
import * as API from "@/services/BackendAPI";
import { getLanguage } from "@/services/LanguageDetection";
import { LinterListResponse } from "@/services/types/api_responses_interfaces";

@Component({
  components: {
    LintCard,
  },
})
export default class LintView extends Vue {
  name = "LintView";
  @Prop({ default: false }) outdated!: boolean;
  @Prop({ default: "Linter" }) linter!: string;
  @Prop({
    default: () => [],
  })
  lints!: Lint[];
  @Prop({
    default: () => ({
      file: { name: "unnamed", path: "unnamed", content: "" },
      language: "auto",
      detectedLanguage: "txt",
      unsaved: false,
      edited: false,
    }),
  })
  fileState!: FileState;

  private availableLinterMappings: LinterListResponse = {};

  created(): void {
    this.fetchAvailableLinters();
  }

  private async fetchAvailableLinters(): Promise<void> {
    const resp: LinterListResponse = await API.getLinters();
    if (resp.errorMessage != undefined) {
      this.$emit("notification", { type: "error", message: resp.errorMessage });
      return;
    }
    this.availableLinterMappings = resp;
  }

  private getLanguagePassthrough(name: string): string {
    return getLanguage(name);
  }
}
</script>

<style scoped>
.lint-view {
  border: var(--v-bg_secondary-base) solid 0;
  border-bottom-right-radius: 5px;

  height: 100%;
  overflow-y: auto;

  scrollbar-color: var(--v-bg_tertiary-lighten1) var(--v-bg_secondary-base);
}

.code-editor {
  height: auto;
}

.outdated-notif {
  position: absolute;
  top: 1em;
  left: 50%;
  transform: translateX(-50%);
  font-weight: bold;
}
</style>
