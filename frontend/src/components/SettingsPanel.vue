<template>
  <div class="settings-panel">
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
    <v-row class="settings-row">
      <secrets-search-settings v-on="$listeners"></secrets-search-settings>
    </v-row>
    <v-row class="settings-row">
      <v-btn color="error" block @click="emitDeleteProject">
        Delete Project
        <v-icon small right>mdi-delete</v-icon>
      </v-btn>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import SecretsSearchSettings from "@/components/SecretsSearchSettings.vue";

@Component({
  components: {
    SecretsSearchSettings,
  },
})
export default class ProjectSettings extends Vue {
  name = "ProjectSettings";
  private linter = "auto";
  private linterList = ["linterA", "linterB", "linterC"];

  private emitLinterSet() {
    if (this.linter == null) {
      this.linter = "auto";
    }
    this.$emit("linter-set", this.linter);
  }

  private emitDeleteProject() {
    console.log("delete project not yet implemented");
  }
}
</script>

<style scoped>
.settings-panel {
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
