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
    <v-icon class="cog-icon" small>mdi-cog</v-icon>
    <v-divider v-if="isExpanded" style="margin-left: 2.1em"></v-divider>
    <div v-if="isExpanded" class="project-label">
      <span style="color: gray; font-size: smaller">Project Settings</span>
      <!--<span style="color: var(--v-primary-base); font-size: smaller">
        {{ activeProjectName }}
      </span>-->
    </div>
    <v-expand-transition>
      <div v-show="isExpanded" class="settings-panel">
        <v-row class="settings-row">
          <v-text-field
            v-model="projectNameEdit"
            class="rename-text-field"
            color="white"
            label="Project Name"
            outlined
            dense
            hide-details="auto"
            @focus="renameHasFocus = true"
            @blur="renameHasFocus = false"
          ></v-text-field>
          <v-tooltip bottom open-delay="1000">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="rename-apply-button"
                color="var(--v-bg_tertiary-lighten3)"
                icon
                outlined
                :disabled="activeProjectName == projectNameEdit"
                v-bind="attrs"
                v-on="on"
                @click="$emit('rename-project', projectNameEdit)"
              >
                <v-icon color="primary">mdi-check</v-icon>
              </v-btn>
            </template>
            <span>Apply New Name</span>
          </v-tooltip>
        </v-row>
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
    <v-divider
      :class="isExpanded ? 'bottom-divider-full' : 'bottom-divider-inset'"
    ></v-divider>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";

@Component({
  components: {},
})
export default class ProjectSettings extends Vue {
  name = "ProjectSettings";
  @Prop({ default: "No Project" }) activeProjectName!: string;
  private projectNameEdit = "No Project";
  private renameHasFocus = false;
  private isExpanded = false;
  private linter = "auto";
  private linterList = ["linterA", "linterB", "linterC"];

  @Watch("activeProjectName")
  private projectNameChanged(): void {
    this.projectNameEdit = this.activeProjectName;
  }

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
.cog-icon {
  position: absolute;
  margin: 2.475em 0.6em;
  color: var(--v-bg_tertiary-lighten1);
}

.bottom-divider-inset {
  margin-left: 2.1em;
  transition: 0.2s;
}

.bottom-divider-full {
  margin-left: 0;
  transition: 0.3s;
}

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
  text-align: right;
}

.rename-text-field {
  margin-right: 0.6em;
}

.v-input--is-focused::v-deep .v-input__slot,
.v-input--is-focused::v-deep .v-label--active {
  color: var(--v-primary-base) !important;
}

.v-input--is-focused::v-deep .v-text-field__slot {
  color: white !important;
}

::v-deep .v-text-field__slot {
  color: lightgrey;
}

.rename-apply-button {
  margin: auto 0;
  height: 40px;
  width: 40px;
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
