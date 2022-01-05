<template>
  <div class="project-overview-panel">
    <v-row style="margin-top: 0">
      <div class="stats-panel">
        <h2 style="text-align: center">Stats Panel Placeholder</h2>
      </div>
    </v-row>
    <v-row style="height: calc(100% - 36px)">
      <div class="secrets-panel">
        <h2 style="text-align: center; position: relative; top: 45%">
          Secret Results Placeholder
        </h2>
      </div>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class ProjectOverview extends Vue {
  name = "ProjectOverview";
}
</script>

<style scoped>
.project-overview-panel {
  background-color: var(--v-bg_secondary-base);
  height: 100%;
}

.stats-panel {
  width: 100%;
  background-color: var(--v-bg_secondary-base);
  border: var(--v-bg_secondary-base) solid 0px;
  border-top-right-radius: 5px !important;
}

.secrets-panel {
  background-color: var(--v-bg_secondary-base);
  width: 100%;
  height: 100%;

  border: var(--v-bg_secondary-base) solid 0 !important;
  border-bottom-right-radius: 5px !important;
}

.custom-text-field {
  width: fit-content;
  min-width: 50px;
}
</style>
