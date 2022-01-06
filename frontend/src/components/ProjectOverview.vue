<template>
  <div class="project-overview-panel">
    <div style="margin-top: 0">
      <div class="d-flex flex-row header">
        <v-btn
          style="position: absolute"
          class="header-component"
          icon
          @click="emitCloseOverview"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
        <h2 class="header-component header-title">
          {{ project.settings.data.name }}
        </h2>
      </div>
    </div>
    <div style="height: 10%">
      <div class="stats-panel">
        <h3 style="text-align: center">Stats Panel Placeholder</h3>
      </div>
    </div>
    <div>
      <v-divider class="centered-divider"></v-divider>
    </div>
    <div style="height: calc(90% - 48px)" class="secrets-panel">
      <v-container class="secrets-container">
        <ul v-for="file in Object.keys(searchResults)" :key="file">
          <h3>{{ file }}</h3>
          <secret-card
            v-for="result in searchResults[file]"
            :key="result.patternId + result.snippet"
            :result="result"
            :pattern="searchPatterns[result.patternId]"
          ></secret-card>
        </ul>
      </v-container>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { Dictionary } from "vue-router/types/router";
import { Project, SearchPatterns, SearchResult } from "./types/interfaces";

import SecretCard from "@/components/SecretCard.vue";

@Component({
  components: {
    SecretCard,
  },
})
export default class ProjectOverview extends Vue {
  name = "ProjectOverview";
  @Prop() project!: Project;
  @Prop({
    default: () => {
      return {};
    },
  })
  searchPatterns!: SearchPatterns;
  @Prop({
    default: () => {
      return {};
    },
  })
  searchResults!: Dictionary<SearchResult[]>;

  private emitCloseOverview(): void {
    this.$emit("close-project-overview");
  }
}
</script>

<style scoped>
.project-overview-panel {
  background-color: var(--v-bg_secondary-base);
  height: 100%;
  padding-left: 0;

  border: var(--v-bg_secondary-base) solid 0;
  border-bottom-right-radius: 5px;
}

.header {
  width: 100%;
  height: 48px;
  background-color: var(--v-bg_tertiary-base);
  border: var(--v-bg_secondary-base) solid 0px;
  border-top-right-radius: 5px;
}

.header-component {
  margin: auto 0.6em;
  align-self: center;
}

.header-title {
  flex-grow: 1;
  text-align: center;
}

.centered-divider {
  margin: -0.5px 0%;
}

.stats-panel {
  width: 100%;
  height: 100%;
  padding: 0.6em;
  background-color: var(--v-bg_secondary-base);
}

.secrets-panel {
  border: var(--v-bg_secondary-base) solid 0;
  border-bottom-right-radius: 5px;
  overflow: hidden;
}

.secrets-container {
  background-color: var(--v-bg_secondary-base);
  width: 100%;
  height: 100%;
  overflow-y: auto;

  scrollbar-color: var(--v-bg_tertiary-lighten1) var(--v-bg_secondary-base);
}

.custom-text-field {
  width: fit-content;
  min-width: 50px;
}
</style>
