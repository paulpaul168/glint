<template>
  <div class="settings-panel">
    <v-row class="settings-row">
      <secrets-search-settings v-on="$listeners"></secrets-search-settings>
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
export default class GlobalSettings extends Vue {
  name = "GlobalSettings";
}
</script>

<style scoped>
.settings-panel {
  align-self: flex-start;
  width: 100%;
}

.settings-row {
  margin: 0.6em;
  justify-content: flex-start;
  width: auto;
}

.dropdown {
  min-width: 7em;
}

.dropdown::v-deep .v-input__icon--clear .v-icon {
  font-size: 1em;
}
</style>
