<template>
  <div class="project-settings-panel">
    <v-row class="settings-row">
      <v-select
        v-model="language"
        class="dropdown"
        dense
        outlined
        label="Language"
        placeholder="auto"
        hide-details="auto"
        clearable
        :menu-props="{ top: true, offsetY: true, nudgeTop: 14 }"
        :items="languageList"
        @change="emitLanguageSet"
      >
        <v-icon slot="append-inner" small>mdi-window-close</v-icon>
      </v-select>
    </v-row>
    <v-row class="settings-row">
      <v-select
        v-model="linter"
        class="dropdown"
        dense
        outlined
        label="Linter"
        placeholder="auto"
        hide-details="auto"
        clearable
        no-data-text="No Linters available for this language"
        :menu-props="{ top: true, offsetY: true, nudgeTop: 14 }"
        :items="linterList"
        @change="emitLinterSet"
      ></v-select>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import { supportedLanguages } from "@/services/LanguageDetection";

@Component({
  components: {},
})
export default class ProjectSettings extends Vue {
  name = "ProjectSettings";
  private language = "auto";
  private linter = "auto";
  private languageList = supportedLanguages;
  private linterList = ["linterA", "linterB", "linterC"];

  private emitLanguageSet() {
    if (this.language == null) {
      this.language = "auto";
    }
    this.$emit("language-set", this.language);
  }

  private emitLinterSet() {
    if (this.linter == null) {
      this.linter = "auto";
    }
    this.$emit("linter-set", this.linter);
  }
}
</script>

<style scoped>
.project-settings-panel {
  align-self: flex-start;
}

.settings-row {
  margin: 0.6em;
  justify-content: flex-start;
}

.dropdown {
  min-width: 7em;
}

.dropdown::v-deep .v-input__icon--clear .v-icon {
  font-size: 1em;
}
</style>
