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
            v-for="pattern in patterns"
            :key="pattern.id"
            class="pattern-row"
          >
            <v-text-field
              v-model="pattern.name"
              class="pattern-name"
              solo
              flat
              dense
              label="Pattern name"
              hide-details="auto"
              :disabled="true"
            >
            </v-text-field>
          </v-row>
        </div>
        <div class="d-flex flex-column regex-col">
          <v-row
            v-for="pattern in patterns"
            :key="pattern.id"
            class="pattern-row"
          >
            <v-text-field
              v-model="pattern.regex"
              class="pattern-regex"
              solo
              flat
              dense
              label="Regex"
              hide-details="auto"
              :disabled="true"
            >
            </v-text-field>
          </v-row>
        </div>
        <div class="d-flex flex-column button-col">
          <v-row
            v-for="pattern in patterns"
            :key="pattern.id"
            class="pattern-row"
          >
            <v-btn icon>
              <v-icon small>mdi-pencil</v-icon>
            </v-btn>
          </v-row>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="secondary" @click="discardSettings">Close</v-btn>
        <v-btn color="primary" @click="storeSettings">Done</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { SearchPattern } from "./types/interfaces";

import * as API from "@/services/BackendAPI";

@Component
export default class SecretsSearchSettings extends Vue {
  name = "SecretsSearchSettings";
  private dialog = false;
  private patterns: SearchPattern[] = [];

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

  private fetchPatterns(): void {
    this.patterns = [
      {
        name: "flag",
        id: "1",
        regex: "/flag{.*}/",
      },
      {
        name: "flag2",
        id: "2",
        regex: "/flag2{.*}/",
      },
    ];
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
}

.pattern-row {
  margin: 0.5em;
}

.pattern-name {
  width: 70px;
  margin-right: 1em;
}

.pattern-regex {
  margin-top: auto;
  margin-bottom: auto;
  font-family: "Fira code", "Fira Mono", "Consolas", "Menlo", "Courier New",
    monospace;
}
</style>
