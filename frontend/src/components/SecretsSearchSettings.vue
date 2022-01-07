<template>
  <v-dialog v-model="dialog" max-width="600">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        class="rounded-md dialog-button"
        color="primary"
        elevation="0"
        block
        v-bind="attrs"
        v-on="on"
      >
        Secret Finder Patterns
      </v-btn>
    </template>

    <v-card>
      <v-card-title>Secrets Search Pattern Settings</v-card-title>
      <v-card-text style="padding-bottom: 0" class="d-flex flex-row">
        <div class="d-flex flex-column name-col">
          <v-row
            v-for="(key, index) in Object.keys(patterns)"
            :key="key"
            class="pattern-row"
          >
            <v-text-field
              v-model="patterns[key].patternName"
              class="pattern-name"
              :rules="[(v) => v.length > 0 || 'Required']"
              outlined
              flat
              dense
              label="Name"
              :disabled="index != editPattern"
            >
            </v-text-field>
          </v-row>
          <v-row v-if="addPatternMode" class="pattern-row">
            <v-text-field
              v-model="newPatternName"
              class="pattern-name"
              :rules="[(v) => v.length > 0 || 'Required']"
              outlined
              flat
              dense
              :error-messages="newPatternName.length > 0 ? '' : 'Required'"
              label="Name"
            >
            </v-text-field>
          </v-row>
        </div>
        <div class="d-flex flex-column regex-col">
          <v-row
            v-for="(key, index) in Object.keys(patterns)"
            :key="key"
            class="pattern-row"
          >
            <v-text-field
              v-model="patterns[key].regex"
              class="pattern-regex"
              :rules="[
                (v) => /^\/.*\/g?i?m?s?u?y?$/.test(v) || 'Enter a valid regex!',
              ]"
              outlined
              flat
              dense
              label="Regex"
              :disabled="index != editPattern"
            >
            </v-text-field>
          </v-row>
          <v-row v-if="addPatternMode" class="pattern-row">
            <v-text-field
              v-model="newPatternRegex"
              class="pattern-regex"
              :rules="[
                (v) => /^\/.*\/g?i?m?s?u?y?$/.test(v) || 'Enter a valid regex!',
              ]"
              outlined
              flat
              dense
              :error-messages="
                newPatternRegex.length > 0 ? '' : 'Enter a valid regex!'
              "
              label="/regex/flags"
            >
            </v-text-field>
          </v-row>
        </div>
        <div class="d-flex flex-column button-col">
          <v-row
            v-for="(key, index) in Object.keys(patterns)"
            :key="key"
            class="pattern-row"
          >
            <v-spacer></v-spacer>
            <v-tooltip bottom open-delay="1000">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  class="pattern-buttons"
                  icon
                  v-bind="attrs"
                  v-on="on"
                  :disabled="
                    !(
                      patterns[key].patternName.length > 0 &&
                      /^\/.*\/g?i?m?s?u?y?$/.test(patterns[key].regex)
                    )
                  "
                  @click="savePatternEdit(index)"
                >
                  <v-icon v-if="index != editPattern" small>mdi-pencil</v-icon>
                  <v-icon v-else small>mdi-check</v-icon>
                </v-btn>
              </template>
              <span v-if="index != editPattern">Edit Pattern</span>
              <span v-else>Finish Pattern Edits</span>
            </v-tooltip>
            <v-tooltip v-if="index == editPattern" bottom open-delay="1000">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  class="pattern-buttons"
                  icon
                  v-bind="attrs"
                  v-on="on"
                  @click="deletePattern(index)"
                >
                  <v-icon small>mdi-delete</v-icon>
                </v-btn>
              </template>
              <span>Delete Pattern</span>
            </v-tooltip>
          </v-row>
          <v-row v-if="addPatternMode" class="pattern-row">
            <v-spacer></v-spacer>
            <v-tooltip bottom open-delay="1000">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  class="pattern-buttons"
                  icon
                  :disabled="
                    !(
                      newPatternName.length > 0 &&
                      /^\/.*\/g?i?m?s?u?y?$/.test(newPatternRegex)
                    )
                  "
                  v-bind="attrs"
                  v-on="on"
                  @click="addPattern"
                >
                  <v-icon small>mdi-check</v-icon>
                </v-btn>
              </template>
              <span>Add Pattern</span>
            </v-tooltip>
            <v-tooltip bottom open-delay="1000">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  class="pattern-buttons"
                  icon
                  v-bind="attrs"
                  v-on="on"
                  @click="
                    addPatternMode = false;
                    newPatternName = '';
                    newPatternRegex = '';
                  "
                >
                  <v-icon small>mdi-close</v-icon>
                </v-btn>
              </template>
              <span>Cancel Pattern Creation</span>
            </v-tooltip>
          </v-row>
        </div>
      </v-card-text>
      <div style="margin-bottom: 1.7em" class="d-flex flex-row">
        <v-btn
          v-if="addPatternMode == false"
          class="add-pattern-button"
          color="primary"
          text
          @click="addPatternMode = true"
        >
          <v-icon left>mdi-plus</v-icon> Create Pattern
        </v-btn>
        <v-spacer></v-spacer>
        <v-tooltip bottom open-delay="1000">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="refresh-patterns-button"
              icon
              color="primary"
              elevation="0"
              v-bind="attrs"
              v-on="on"
              :loading="fetchingPatterns"
              @click="fetchPatterns"
            >
              <template v-slot:loader>
                <span class="custom-loader">
                  <v-icon color="primary">mdi-cached</v-icon>
                </span>
              </template>
              <v-icon>mdi-cached</v-icon>
            </v-btn>
          </template>
          <span>Reload Patterns</span>
        </v-tooltip>
      </div>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="action-button" color="primary" @click="dialog = false">
          Done
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { SearchPatterns } from "./types/interfaces";

import * as API from "@/services/BackendAPI";
import { SearchPatternsResponse } from "@/services/types/api_responses_interfaces";
import { Dictionary } from "vue-router/types/router";
@Component
export default class SecretsSearchSettings extends Vue {
  name = "SecretsSearchSettings";
  private dialog = false;
  private patterns: SearchPatterns = {};
  private patternsValidity: Dictionary<{
    nameValid: boolean;
    patternValid: boolean;
  }> = {};
  private allPatternsValid = true;
  private editPattern = -1;

  private addPatternMode = false;
  private newPatternName = "";
  private newPatternRegex = "";

  private fetchingPatterns = false;

  private discardSettings(): void {
    console.log("discarding secrets settings but not implemented yet");
    this.dialog = false;
  }

  private storeSettings(): void {
    console.log("storing secrets settings but not implemented yet");
    this.dialog = false;
  }

  created(): void {
    this.fetchPatterns();
  }

  @Watch("patterns")
  private createValidityEntries(): void {
    this.patternsValidity = {};
    for (const key of Object.keys(this.patterns)) {
      this.patternsValidity[key] = { nameValid: true, patternValid: true };
    }
  }

  private async fetchPatterns(): Promise<void> {
    this.fetchingPatterns = true;
    const resp: SearchPatternsResponse = await API.getSearchPatterns();
    if (resp.errorMessage != undefined) {
      this.$emit("notification", { type: "error", message: resp.errorMessage });
      this.fetchingPatterns = false;
      return;
    }
    this.createValidityEntries();
    this.patterns = resp;
    this.emitSetPatterns();
    this.fetchingPatterns = false;
  }

  private emitSetPatterns(): void {
    this.$emit("set-patterns", this.patterns);
  }

  private async savePatternEdit(index: number): Promise<void> {
    this.editPattern != index
      ? (this.editPattern = index)
      : (this.editPattern = -1);

    const result = await API.setSearchPattern(
      this.patterns[Object.keys(this.patterns)[index]],
      Object.keys(this.patterns)[index]
    );
    if (result.errorMessage != undefined) {
      this.$emit("notification", {
        type: "error",
        message: result.errorMessage,
      });
      return;
    }
    this.emitSetPatterns();
    this.fetchPatterns();
  }

  private async addPattern(): Promise<void> {
    const result = await API.setSearchPattern({
      patternName: this.newPatternName,
      regex: this.newPatternRegex,
    });
    if (result.errorMessage != undefined) {
      this.$emit("notification", {
        type: "error",
        message: result.errorMessage,
      });
      return;
    }
    this.addPatternMode = false;
    this.emitSetPatterns();
    this.fetchPatterns();
  }

  private async deletePattern(index: number): Promise<void> {
    const result = await API.deleteSearchPattern(
      Object.keys(this.patterns)[index]
    );
    if (result.errorMessage != undefined) {
      this.$emit("notification", {
        type: "error",
        message: result.errorMessage,
      });
      return;
    }
    this.editPattern = -1;
    delete this.patterns[Object.keys(this.patterns)[index]];
    this.$forceUpdate();
    this.emitSetPatterns();
  }
}
</script>

<style scoped>
.dialog-button {
  text-transform: none;
}

.action-button {
  margin-left: 8px;
}

.add-pattern-button {
  margin-left: 1.8em;
}

.refresh-patterns-button {
  margin-right: 2.5em;
}

.name-col {
  flex-grow: 1;
}

.regex-col {
  flex-grow: 3;
}

.button-col {
  flex-grow: 0;
  min-width: 100px;
}

.pattern-row {
  margin: 0 0.5em;
}

.pattern-name {
  width: 70px;
  transition: 0.2s;
}

.pattern-name:disabled {
  transition: 0.1s;
}

.pattern-regex {
  margin-top: auto;
  margin-bottom: auto;
  font-family: "Fira code", "Fira Mono", "Consolas", "Menlo", "Courier New",
    monospace;
}

.pattern-buttons {
  margin-right: 0.2em;
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
