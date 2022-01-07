<template>
  <div class="d-flex flex-column main-content-pane projects-panel">
    <div class="projects-container">
      <project-tree-view
        v-for="(project, index) of projects"
        :key="project.settings.data.projectId"
        :active="index == activeProject"
        :lastProject="projects.length == 1"
        :project="project"
        @request-active="emitSetActiveProject($event)"
        v-on="$listeners"
      ></project-tree-view>
    </div>
    <v-divider class="centered-divider"></v-divider>
    <div class="d-flex flex-row project-list-buttons">
      <v-tooltip bottom open-delay="1000">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            class="project-button"
            icon
            color="primary"
            elevation="0"
            v-bind="attrs"
            v-on="on"
            @click="$emit('create-project')"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>
        <span>Create Project</span>
      </v-tooltip>
      <v-tooltip bottom open-delay="1000">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            class="project-button"
            icon
            color="primary"
            elevation="0"
            v-bind="attrs"
            v-on="on"
            :loading="fetchingProjects"
            @click="$emit('refresh-projects')"
          >
            <template v-slot:loader>
              <span class="custom-loader">
                <v-icon color="primary">mdi-cached</v-icon>
              </span>
            </template>
            <v-icon>mdi-cached</v-icon>
          </v-btn>
        </template>
        <span>Reload Project List</span>
      </v-tooltip>
      <v-tooltip bottom open-delay="1000">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            class="project-button"
            icon
            color="primary"
            elevation="0"
            v-bind="attrs"
            v-on="on"
            @click="$emit('toggle-project-info')"
          >
            <v-icon>mdi-information-outline</v-icon>
          </v-btn>
        </template>
        <span>Toggle Project Info</span>
      </v-tooltip>
    </div>

    <v-spacer></v-spacer>
    <project-settings
      :project="projects[activeProject]"
      :activeProjectName="projects[activeProject].settings.data.name"
      v-on="$listeners"
    ></project-settings>
    <settings-panel v-on="$listeners"></settings-panel>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import SettingsPanel from "@/components/SettingsPanel.vue";
import ProjectSettings from "@/components/ProjectSettings.vue";
import ProjectTreeView from "@/components/file_tree/ProjectTreeView.vue";
import { Project } from "./types/interfaces";

@Component({
  components: {
    SettingsPanel,
    ProjectSettings,
    ProjectTreeView,
  },
})
export default class ProjectList extends Vue {
  @Prop({ default: false }) fetchingProjects!: boolean;
  @Prop() projects!: Project[];
  @Prop({ default: 0 }) activeProject!: number;
  private internalIdentifier = 0;

  private emitSetActiveProject(projectId: string): void {
    this.projects.forEach((project, index) => {
      if (project.settings.data.projectId == projectId) {
        this.$emit("set-active-project", index);
        return;
      }
    });
  }
}
</script>

<style scoped>
.projects-panel {
  min-width: 250px;
  width: fit-content;
  background-color: var(--v-bg_tertiary-base);
  border: var(--v-bg_tertiary-base) solid 0;
  border-bottom-left-radius: 5px;
  border-top-left-radius: 5px;
  padding-top: 9.8px;
}

.projects-container {
  min-width: 238px;
  width: fit-content;
  margin-left: 12px;
  padding: 0;
  border-radius: 0;
  overflow-y: scroll;
  scrollbar-color: var(--v-bg_tertiary-lighten1) var(--v-bg_tertiary-base);
  border-bottom-right-radius: 5px;
}

.active-project-label {
  text-align: center;
  color: var(--v-primary-base);
}

.centered-divider {
  margin: 0.4em 10%;
}

.project-list-buttons {
  margin: 0.2em 12px;
  margin-bottom: 2em;
  flex-grow: 0;
  justify-content: center;
}

.project-button {
  margin: 0 0.2em;
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
