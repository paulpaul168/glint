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
        Linter Mappings
      </v-btn>
    </template>

    <v-card>
      <v-card-title>Linter Mappings</v-card-title>
      <v-card-text style="padding-bottom: 0">
        <v-row
          v-for="mapping of internalMappings"
          :key="mapping.id"
          class="mapping-row"
        >
          <v-select
            v-model="mapping.language"
            class="dropdown"
            dense
            outlined
            label="Language"
            placeholder="Language"
            hide-details="auto"
            clearable
            append-icon="mdi-chevron-down"
            no-data-text="No more languages available"
            :menu-props="{
              bottom: true,
              offsetY: true,
              nudgeBottom: 8,
              transition: 'scroll-y-transition',
            }"
            :items="[mapping.language].concat(remainingLanguages)"
          ></v-select>
          <v-select
            v-model="mapping.linter"
            class="dropdown"
            dense
            outlined
            label="Linter"
            placeholder="Linter"
            hide-details="auto"
            clearable
            append-icon="mdi-chevron-down"
            no-data-text="No Linters available for this language"
            :menu-props="{
              bottom: true,
              offsetY: true,
              nudgeBottom: 8,
              transition: 'scroll-y-transition',
            }"
            :items="availableLinterMappings[mapping.language]"
            @change="saveMappingEdit"
          ></v-select>
          <v-spacer></v-spacer>
          <v-tooltip bottom open-delay="1000">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="delete-mapping-button"
                icon
                v-bind="attrs"
                v-on="on"
                @click="deleteMapping(mapping.id)"
              >
                <v-icon small>mdi-delete</v-icon>
              </v-btn>
            </template>
            <span>Delete Mapping</span>
          </v-tooltip>
        </v-row>
        <v-row v-if="addMappingMode" class="mapping-row">
          <v-select
            v-model="newMappingLanguage"
            class="dropdown"
            dense
            outlined
            label="Language"
            placeholder="Language"
            hide-details="auto"
            clearable
            append-icon="mdi-chevron-down"
            no-data-text="No more languages available"
            :menu-props="{
              bottom: true,
              offsetY: true,
              nudgeBottom: 8,
              transition: 'scroll-y-transition',
            }"
            :items="remainingLanguages"
          ></v-select>
          <v-select
            v-model="newMappingLinter"
            class="dropdown"
            dense
            outlined
            label="Linter"
            placeholder="Linter"
            hide-details="auto"
            clearable
            :disabled="newMappingLanguage == null || newMappingLanguage == ''"
            append-icon="mdi-chevron-down"
            no-data-text="No Linters available for this language"
            :menu-props="{
              bottom: true,
              offsetY: true,
              nudgeBottom: 8,
              transition: 'scroll-y-transition',
            }"
            :items="availableLinterMappings[newMappingLanguage]"
            @change="
              saveMappingEdit();
              addMappingMode = false;
              newMappingLanguage = '';
              newMappingLinter = '';
            "
          ></v-select>
          <v-spacer></v-spacer>
          <v-tooltip bottom open-delay="1000">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="delete-mapping-button"
                icon
                v-bind="attrs"
                v-on="on"
                @click="addMappingMode = false"
              >
                <v-icon small>mdi-close</v-icon>
              </v-btn>
            </template>
            <span>Cancel Mapping Creation</span>
          </v-tooltip>
        </v-row>
      </v-card-text>
      <div style="margin-bottom: 1.7em" class="d-flex flex-row">
        <v-btn
          v-if="addMappingMode == false"
          class="add-mapping-button"
          color="primary"
          text
          @click="addMappingMode = true"
        >
          <v-icon left>mdi-plus</v-icon> Create Mapping
        </v-btn>
        <v-spacer></v-spacer>
        <v-tooltip bottom open-delay="1000">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="refresh-mappings-button"
              icon
              color="primary"
              elevation="0"
              v-bind="attrs"
              v-on="on"
              :loading="fetchingMappings"
              @click="fetchMappings"
            >
              <template v-slot:loader>
                <span class="custom-loader">
                  <v-icon color="primary">mdi-cached</v-icon>
                </span>
              </template>
              <v-icon>mdi-cached</v-icon>
            </v-btn>
          </template>
          <span>Reload Mappings</span>
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
import { Component, Prop, Vue, Watch } from "vue-property-decorator";

import * as API from "@/services/BackendAPI";
import { AvailableLinters, LinterMapping } from "./types/interfaces";
import {
  LinterListResponse,
  ProjectDataResponse,
  ProjectResponse,
} from "@/services/types/api_responses_interfaces";
import { supportedLanguages } from "@/services/LanguageDetection";

@Component
export default class LinterMappingsSettings extends Vue {
  name = "LinterMappingsSettings";
  private dialog = false;

  @Prop({
    default: () => {
      return {
        name: "",
        projectId: "",
        projectUrl: new URL(API.apiAddress),
        sourcesUrl: new URL(API.apiAddress),
        lintUrl: new URL(API.apiAddress),
      };
    },
  })
  projectMetadata!: ProjectResponse;
  @Prop({
    default: () => {
      return {};
    },
  })
  mappings!: LinterMapping;
  private internalMappings: { id: number; language: string; linter: string }[] =
    [];
  private internalId = 0;

  private availableLinterMappings: AvailableLinters = {};
  private availableLanguages: string[] = supportedLanguages;
  private remainingLanguages: string[] = supportedLanguages;

  private addMappingMode = false;
  private newMappingLanguage = "";
  private newMappingLinter = "";

  private fetchingMappings = false;

  created(): void {
    this.fetchAvailableMappings();
  }

  @Watch("projectMetadata")
  private metadataChange(): void {
    this.fetchMappings();
  }

  @Watch("mappings")
  private mappingsChange(): void {
    this.internalMappings = [];
    for (const key of Object.keys(this.mappings)) {
      this.internalMappings.push({
        id: this.internalId++,
        language: key,
        linter: this.mappings[key],
      });
    }
    this.updateRemainingLanguages();
  }

  private updateRemainingLanguages(): void {
    const newRemainingLanguages = [...supportedLanguages];
    for (const mappingEntry of this.internalMappings) {
      newRemainingLanguages.forEach((language, index) => {
        if (mappingEntry.language == language) {
          newRemainingLanguages.splice(index, 1);
        }
      });
    }
    this.remainingLanguages = newRemainingLanguages;
  }

  private constructMappingsFromList(
    list: { id: number; language: string; linter: string }[]
  ): LinterMapping {
    const returnMapping: LinterMapping = {};
    for (const mappingEntry of list) {
      if (mappingEntry.language == null) {
        continue;
      }
      returnMapping[mappingEntry.language] =
        mappingEntry.linter == null ? "auto" : mappingEntry.linter;
    }
    return returnMapping;
  }

  private async fetchMappings(): Promise<void> {
    this.fetchingMappings = true;
    if (
      this.projectMetadata.projectId == undefined ||
      this.projectMetadata.projectId == ""
    ) {
      return;
    }
    const resp: ProjectDataResponse = await API.getProjectData(
      this.projectMetadata.projectId
    );
    if (resp.errorMessage != undefined) {
      this.$emit("notification", { type: "error", message: resp.errorMessage });
      this.fetchingMappings = false;
      return;
    }
    this.updateRemainingLanguages();
    this.$emit("set-linter-mappings", resp.linters);
    this.fetchingMappings = false;
  }

  private async fetchAvailableMappings(): Promise<void> {
    this.fetchingMappings = true;
    const resp: LinterListResponse = await API.getLinters();
    if (resp.errorMessage != undefined) {
      this.$emit("notification", { type: "error", message: resp.errorMessage });
      this.fetchingMappings = false;
      return;
    }
    this.availableLinterMappings = resp;
    this.fetchingMappings = false;
  }

  private async saveMappingEdit(): Promise<void> {
    if (this.addMappingMode) {
      this.internalMappings.push({
        id: this.internalId++,
        language: this.newMappingLanguage,
        linter: this.newMappingLinter,
      });
    }
    const result = await API.editProject(this.projectMetadata.projectId, {
      name: null,
      linters: this.constructMappingsFromList(this.internalMappings),
    });
    if (result.errorMessage != undefined) {
      this.$emit("notification", {
        type: "error",
        message: result.errorMessage,
      });
      return;
    }
    this.fetchMappings();
  }

  private async addMapping(): Promise<void> {
    this.internalMappings.push({
      id: this.internalId++,
      language: this.newMappingLanguage,
      linter: this.newMappingLinter,
    });
    this.updateRemainingLanguages();
    this.saveMappingEdit();
  }

  private async deleteMapping(id: number): Promise<void> {
    let foundIndex = -1;
    this.internalMappings.forEach((mapping, index) => {
      if (mapping.id == id) {
        foundIndex = index;
        return;
      }
    });
    if (foundIndex != -1) {
      this.internalMappings.splice(foundIndex, 1);
      this.saveMappingEdit();
    } else {
      console.log("Tried deleting a mapping ID that didn't exist");
      this.$emit("notification", {
        type: "error",
        message: "Tried deleting a mapping that didn't exist",
      });
    }
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

.add-mapping-button {
  margin-left: 2.2em;
}

.delete-mapping-button {
  margin: auto 0;
}

.refresh-mappings-button {
  margin-right: 2.2em;
}

.mapping-row {
  margin: 1em 0.5em;
}

.dropdown {
  margin-right: 1em;
  min-width: 7em;
  max-width: 40%;
}

.dropdown::v-deep .v-input__icon--clear .v-icon {
  font-size: 1em;
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
