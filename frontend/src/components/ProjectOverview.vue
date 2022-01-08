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
      <v-divider style="margin: -0.5px 0"></v-divider>
    </div>
    <div style="height: calc(90% - 48px)" class="secrets-panel">
      <div v-if="resultsSum > 0" class="secrets-header">
        <h3 style="color: grey">Found {{ resultsSum }} Secrets</h3>
      </div>
      <div style="height: 100%" v-else>
        <h3 style="text-align: center; position: relative; top: 45%">
          No Secrets were found in this Project
        </h3>
      </div>
      <v-tooltip bottom open-delay="1000">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            class="secret-search-button"
            small
            elevation="0"
            color="transparent"
            v-bind="attrs"
            v-on="on"
            :loading="searchingForSecrets"
            @click="$emit('start-secret-search')"
          >
            <template v-slot:loader>
              <span class="custom-loader">
                <v-icon>mdi-cached</v-icon>
              </span>
            </template>
            <v-icon small>mdi-cached</v-icon>
          </v-btn>
        </template>
        <span>Refresh Search</span>
      </v-tooltip>
      <v-container class="secrets-container">
        <ul
          v-for="(file, index) in Object.keys(searchResults)"
          :key="file"
          style="padding-left: 12px"
        >
          <v-divider v-if="index != 0" class="centered-divider"></v-divider>
          <div v-if="searchResults[file].length > 0">
            <div class="d-flex flex-row">
              <v-btn icon :ripple="false" @click="toggleFileExpansion(file)">
                <v-icon
                  :class="
                    fileResultsExpanded[file] ? 'chevron-open' : 'chevron-close'
                  "
                  small
                >
                  mdi-chevron-right
                </v-icon>
              </v-btn>
              <span class="file-header-text text-h6 header-component">
                {{ file }}
              </span>
              <v-spacer></v-spacer>
              <span class="file-secrets-summary text-caption">
                <span style="color: grey">Matches:&nbsp;</span>
                <span style="color: var(--v-primary-base)">
                  {{ searchResults[file].length }}
                </span>
              </span>
            </div>
            <v-expand-transition>
              <div v-show="fileResultsExpanded[file]">
                <secret-card
                  v-for="result in searchResults[file]"
                  :key="
                    result.patternId +
                    '' +
                    result.line +
                    '' +
                    result.col +
                    result.snippet
                  "
                  :result="result"
                  :pattern="searchPatterns[result.patternId]"
                  v-on="$listeners"
                ></secret-card>
              </div>
            </v-expand-transition>
          </div>
        </ul>
      </v-container>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
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
  @Prop({ default: false }) searchingForSecrets!: boolean;
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

  private fileResultsExpanded: Dictionary<boolean> = {};
  private resultsSum = 0;

  @Watch("searchResults", { immediate: true })
  private resultsChanged(): void {
    this.resultsSum = 0;
    for (const key of Object.keys(this.searchResults)) {
      this.fileResultsExpanded[key] = true;
      this.resultsSum += this.searchResults[key].length;
    }
  }

  private toggleFileExpansion(file: string): void {
    this.fileResultsExpanded[file] = !this.fileResultsExpanded[file];
    this.$forceUpdate();
    //force update has to be done, otherwise v-for caches the element and doesn't re-render it (in the new expand state) until another DOM change
  }

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
  margin: 2em 5.7%;
}

.stats-panel {
  width: 100%;
  height: 100%;
  padding: 0.6em;
  background-color: var(--v-bg_secondary-base);
}

.secrets-panel {
  position: relative;
  border: var(--v-bg_secondary-base) solid 0;
  border-bottom-right-radius: 5px;
  overflow: hidden;
}

.secret-search-button {
  z-index: 10;
  position: absolute;
  top: 0.3em;
  right: 1em;
}

.secrets-header {
  z-index: 10;
  position: absolute;
  text-align: center;
  top: 0.3em;
  left: 50%;
  transform: translateX(-50%);
}

.secrets-container {
  background-color: var(--v-bg_secondary-base);
  width: 100%;
  height: 100%;
  overflow-y: auto;

  scrollbar-color: var(--v-bg_tertiary-lighten1) var(--v-bg_secondary-base);

  padding-top: 2em;
}

.file-header-text {
  margin: 0 0.6em;
}

.file-secrets-summary {
  margin-left: 1em;
  margin-bottom: 0.45em;
  margin-right: 16px;
  align-self: flex-end;
}

.chevron-open {
  transform: rotate(90deg);
  transition: 0.3s;
}

.chevron-close {
  transition: 0.2s;
}

.custom-text-field {
  width: fit-content;
  min-width: 50px;
}

.custom-loader {
  animation: loader 1s infinite;
}
@-moz-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(-360deg);
  }
}
@-webkit-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(-360deg);
  }
}
@-o-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(-360deg);
  }
}
@keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(-360deg);
  }
}
</style>
