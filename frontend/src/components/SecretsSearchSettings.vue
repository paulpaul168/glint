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
      <v-card-text class="d-flex flex-row">
        <div class="d-flex flex-column name-col">
          <v-row
            v-for="(key, index) in Object.keys(patterns)"
            :key="key"
            class="pattern-row"
          >
            <v-text-field
              v-model="patterns[key].name"
              class="pattern-name"
              :background-color="index == editPattern ? 'bg_tertiary' : ''"
              :rules="[(v) => v.length > 0 || 'Required']"
              solo
              flat
              dense
              label="Pattern name"
              :disabled="index != editPattern"
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
                (v) => {
                  const valid = /^\/.*\/g?i?m?s?u?y?$/.test(v);
                  if (!valid) {
                    patternsValidity[key].patternValid = false;
                    return 'Enter a valid regex!';
                  }
                  patternsValidity[key].patternValid = true;
                  return true;
                },
              ]"
              :background-color="index == editPattern ? 'bg_tertiary' : ''"
              solo
              flat
              dense
              label="Regex"
              :disabled="index != editPattern"
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
                    index == editPattern &&
                    !(
                      patternsValidity[key].nameValid == false ||
                      patternsValidity[key].patternValid == false
                    )
                  "
                  @click="
                    editPattern != index
                      ? (editPattern = index)
                      : (editPattern = -1)
                  "
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
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="secondary" @click="discardSettings">
          Discard Changes
        </v-btn>
        <v-tooltip>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              :disabled="editPattern != -1"
              v-bind="attrs"
              v-on="on"
              @click="storeSettings"
            >
              Save
            </v-btn>
          </template>
          <span v-if="editPattern != -1">Finish all Pattern edits!</span>
        </v-tooltip>
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
    const resp: SearchPatternsResponse = await API.getSearchPatterns();
    if (resp.errorMessage != undefined) {
      this.$emit("notification", { type: "error", message: resp.errorMessage });
      //the following pattern assignment is just for debugging purposes while the backend doesn't support this yet
      this.patterns = {
        "1": {
          name: "flag",
          regex: "/urllib.parse/",
        },
        "2": {
          name: "flag2",
          regex: "/flag2{.*}/",
        },
      };
      this.$emit("set-patterns", this.patterns);
      return;
    }
    this.patterns = {
      "1": {
        name: "flag",
        regex: "/urllib.parse/",
      },
      "2": {
        name: "flag2",
        regex: "/flag2{.*}/",
      },
    };
    this.$emit("set-patterns", resp.patterns);
  }

  private setPatterns(): void {
    console.log("set patterns not implemented yet");
  }

  private deletePattern(): void {
    console.log("delete pattern but not implemented yet");
  }

  private addPattern(): void {
    console.log("add pattern but not implemented yet");
  }
}
</script>

<style scoped>
.dialog-button {
  text-transform: none;
}

.name-col {
  flex-grow: 1;
}

.regex-col {
  flex-grow: 6;
}

.button-col {
  flex-grow: 0;
  min-width: 100px;
}

.pattern-row {
  margin: 0.5em;
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
</style>
