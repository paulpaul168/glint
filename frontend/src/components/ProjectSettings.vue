<template>
  <div class="d-flex flex-column">
    <v-tooltip top open-delay="1000">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          class="toggle-button"
          icon
          v-bind="attrs"
          v-on="on"
          @click="isExpanded = !isExpanded"
        >
          <v-icon :class="isExpanded ? 'settings-open' : 'settings-close'">
            mdi-chevron-up
          </v-icon>
        </v-btn>
      </template>
      <span v-if="isExpanded">Hide Project Settings</span>
      <span v-else>Show Project Settings</span>
    </v-tooltip>
    <v-divider v-if="isExpanded"></v-divider>
    <div v-if="isExpanded" class="project-label">
      <span style="color: gray; font-size: smaller">Project Settings: </span>
      <span style="color: var(--v-primary-base); font-size: smaller">
        {{ activeProjectName }}
      </span>
    </div>
    <v-expand-transition>
      <div v-show="isExpanded" class="settings-panel">
        <v-row class="settings-row">
          <v-select
            style="width: 226px"
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
          <v-btn color="error" block @click="emitDeleteProject">
            Delete Project
            <v-icon small right>mdi-delete</v-icon>
          </v-btn>
        </v-row>
      </div>
    </v-expand-transition>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class ProjectSettings extends Vue {
  name = "ProjectSettings";
  @Prop({ default: "No Project" }) activeProjectName!: string;
  private isExpanded = false;
  private linter = "auto";
  private linterList = ["linterA", "linterB", "linterC"];

  private emitLinterSet() {
    if (this.linter == null) {
      this.linter = "auto";
    }
    this.$emit("linter-set", this.linter);
  }

  private emitDeleteProject() {
    this.$emit("delete-project");
  }
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

.project-label {
  margin: 0 0.6em;
  margin-bottom: -0.4em;
}

.toggle-button {
  align-self: center;
  margin: 0.4em 0;
}

.settings-open {
  transform: scaleY(-1);
  transition: 0.4s;
}

.settings-close {
  transform: scaleY(1);
  transition: 0.3s;
}

.dropdown {
  min-width: 7em;
}

.dropdown::v-deep .v-input__icon--clear .v-icon {
  font-size: 1em;
}
</style>
