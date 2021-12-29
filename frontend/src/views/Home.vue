<template>
  <div class="d-flex flex-row main-pane">
    <div class="project-list">
      <project-list
        :projects="activeProjects"
        @set-active-project="activeProject = $event"
        @linter-set="passLinter"
        @notification="passNotification"
      />
    </div>
    <div class="content-view">
      <content-view
        :project="activeProjects[activeProject]"
        :linter="linter"
        @notification="passNotification"
        @new-project="addProject"
      />
    </div>
    <global-notifier :notification="notification"></global-notifier>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import * as API from "@/services/BackendAPI";
import ContentView from "@/components/ContentView.vue";
import ProjectList from "@/components/ProjectList.vue";
import GlobalNotifier from "@/components/GlobalNotifier.vue";

import {
  CreateProjectEvent,
  FileHandle,
  Notification,
  Project,
} from "@/components/types/interfaces";
import { apiAddress } from "@/services/BackendAPI";
import { getLanguage } from "@/services/LanguageDetection";

@Component({
  components: {
    ContentView,
    ProjectList,
    GlobalNotifier,
  },
})
export default class Home extends Vue {
  name = "Home";

  private activeProject = 0;
  private activeProjects: Project[] = [
    {
      settings: {
        data: {
          name: "No Project",
          projectId: "1",
          projectUrl: new URL(apiAddress),
          sourcesUrl: new URL(apiAddress),
          lintUrl: new URL(apiAddress),
        },
        language: "auto",
        linter: "auto",
      },
      files: [
        {
          id: 0,
          edited: false,
          unsaved: false,
          language: "auto",
          detectedLanguage: "txt",
          file: { name: "unnamed", path: "unnamed", content: "" },
        },
      ],
      lintData: {
        status: "",
        linter: "unknown",
        lintFiles: [],
      },
      viewMode: "files",
      remainingLintChecks: 5,
    },
    /*{
      settings: {
        data: {
          name: "New Project2",
          projectId: "2",
          projectUrl: new URL(apiAddress),
          sourcesUrl: new URL(apiAddress),
          lintUrl: new URL(apiAddress),
        },
        language: "auto",
        linter: "auto",
      },
      files: [],
      lintData: {
        status: "",
        linter: "unknown",
        lintFiles: [],
      },
    },*/
  ];

  private linter = "auto";

  private async createProject(event: CreateProjectEvent): Promise<void> {
    const project: Project = {
      settings: {
        data: {
          name: "No Project",
          projectId: "",
          projectUrl: new URL(apiAddress),
          sourcesUrl: new URL(apiAddress),
          lintUrl: new URL(apiAddress),
        },
        language: "auto",
        linter: "auto",
      },
      files: [],
      lintData: {
        status: "",
        linter: "unknown",
        lintFiles: [],
      },
      viewMode: "files",
      remainingLintChecks: 5,
    };
    //get files from user file event and show it in UI
    if (event.files.length == 0) {
      project.files = [
        {
          edited: false,
          unsaved: false,
          language: "auto",
          detectedLanguage: "txt",
          file: { name: "unnamed", path: "unnamed", content: "" },
        },
      ];
    } else {
      project.files = [];
      for (let file of event.files) {
        project.files.push({
          edited: false,
          unsaved: false,
          language: "auto",
          detectedLanguage: getLanguage(file.name),
          file: file,
        });
      }

      //upload files to backend
      //this.uploading = true;
      //extract file handles from file states
      let fileHandles: FileHandle[] = [];
      for (const fileState of project.files) {
        fileHandles.push(fileState.file);
      }
      let result = await API.submitProject({
        name: event.projectName,
        files: fileHandles,
        language: "auto",
        linter: "auto",
      });
      if (result.errorMessage != undefined) {
        console.log(result.errorMessage);
        //this.uploading = false;
        project.files = [
          {
            edited: false,
            unsaved: false,
            language: "auto",
            detectedLanguage: "txt",
            file: { name: "unnamed", path: "unnamed", content: "" },
          },
        ];
        this.$emit("notification", {
          type: "error",
          message: result.errorMessage,
        });
        return;
      }
      project.settings.data = result;
      //this.uploading = false;
      /*this.$emit("new-project", {
        settings: this.projectData,
        files: this.fileStates,
      });*/

      //add current project variable to active projects which also sets the current active project to its index
      const projectIndex = this.addProject(project);

      //set interval for asking for lint status every second. handler has to deactivate asking for lint results on receiving results (or an error)
      this.activeProjects[projectIndex].lintData.status = "processing";
      this.activeProjects[projectIndex].lintCheckTimer = setInterval(
        this.handleLintTimer,
        1000,
        projectIndex
      );
    }
  }

  private addProject(newProject: Project): number {
    if (
      this.activeProjects.length == 1 &&
      this.activeProjects[0].settings.data.name == "No Project"
    ) {
      this.activeProjects = [];
    }
    this.activeProjects.push(newProject);
    this.activeProject = this.activeProjects.length - 1; //may want to reconsider and not set the new project as active by default
    return this.activeProjects.length - 1;
  }

  private async handleLintTimer(projectIndex: number) {
    let remainingChecks = 5;
    if (this.activeProjects[projectIndex].remainingLintChecks != undefined) {
      remainingChecks = this.activeProjects[projectIndex].remainingLintChecks as number;
    }
    if (remainingChecks > 0) {
      remainingChecks--;
      this.activeProjects[projectIndex].lintData = await API.getLint(
        this.activeProjects[projectIndex].settings.data.projectId
      );

      if (this.activeProjects[projectIndex].lintData.status != "processing") {
        clearInterval(this.activeProjects[projectIndex].lintCheckTimer);
        if (this.activeProjects[projectIndex].lintData.status != "done") {
          this.$emit("notification", {
            type: "error",
            message: this.activeProjects[projectIndex].lintData.errorMessage,
          });
        }
      }
    } else {
      clearInterval(this.activeProjects[projectIndex].lintCheckTimer);
      this.$emit("notification", {
        type: "info",
        message:
          "Fetching lint results timed out. Server may still be processing, you can retry.",
      });
    }
    this.activeProjects[projectIndex].remainingLintChecks = remainingChecks;
  }

  private notification: Notification = {
    type: "info",
    message: "Empty Message",
    timeout: 3000,
  };
  private passNotification(newNotification: Notification) {
    this.notification = newNotification;
  }

  private passLinter(linter: string) {
    this.linter = linter;
  }
}
</script>

<style>
.main-pane {
  width: 100%;
  margin: auto;
  height: 100%;
  /*height: calc(97vh - 56px);*/
}

.main-content-pane {
  height: 100%;
}

.project-list {
  max-width: 250px;
  min-width: 250px;
  /*min-width: 200px; the automatic content based resizing doesn't quite work, fixed size is better for now*/
  flex: 1 1 content;
}

.content-view {
  flex-grow: 20;
}
</style>
