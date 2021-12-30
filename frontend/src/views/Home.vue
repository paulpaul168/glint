<template>
  <div class="d-flex flex-row main-pane">
    <div class="project-list">
      <project-list
        :projects="activeProjects"
        :activeProject="activeProject"
        @set-active-project="activeProject = $event"
        @linter-set="passLinter"
        @notification="passNotification"
      />
    </div>
    <div class="content-view">
      <content-view
        :project="activeProjects[activeProject]"
        :uploading="false"
        @notification="passNotification"
        @files-change="uploadFileChanges"
        @open-files-change="storeOpenFileChanges"
        @retry-get-lint="setGetLintTries"
        @create-project-event="createProject($event)"
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
  FileChangeEvent,
  FileHandle,
  FileState,
  Notification,
  OpenFileChangeEvent,
  Project,
} from "@/components/types/interfaces";
import { getLanguage } from "@/services/LanguageDetection";
import { SubmitProject } from "@/services/types/api_requests_interfaces";
import { ProjectResponse } from "@/services/types/api_responses_interfaces";

@Component({
  components: {
    ContentView,
    ProjectList,
    GlobalNotifier,
  },
})
export default class Home extends Vue {
  name = "Home";

  private uploading = false; //todo this should be moved inside the project structure, if two different projects issue uploading shit could get weird
  private activeProject = 0;
  private activeProjects: Project[] = [
    {
      settings: {
        data: {
          name: "No Project",
          projectId: "1",
          projectUrl: new URL(API.apiAddress),
          sourcesUrl: new URL(API.apiAddress),
          lintUrl: new URL(API.apiAddress),
        },
        language: "auto",
        linter: "auto",
      },
      files: [],
      openFiles: [],
      activeFile: 0,
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
          projectUrl: new URL(API.apiAddress),
          sourcesUrl: new URL(API.apiAddress),
          lintUrl: new URL(API.apiAddress),
        },
        language: "auto",
        linter: "auto",
      },
      files: [
        {
          edited: false,
          unsaved: false,
          language: "auto",
          detectedLanguage: "txt",
          file: { name: "oh.py", path: "oh.py", content: "halloooooo = 5" },
        },
      ],
      openFiles: [
        {
          id: 0,
          edited: false,
          unsaved: false,
          language: "auto",
          detectedLanguage: "txt",
          file: { name: "oh.py", path: "oh.py", content: "halloooooo = 5" },
        },
      ],
      activeFile: 0,
      lintData: {
        status: "",
        linter: "unknown",
        lintFiles: [],
      },
      viewMode: "files",
      remainingLintChecks: 5,
    },*/
  ];
  private internalFileId = 0;

  private linter = "auto";

  private async createProject(event: CreateProjectEvent): Promise<void> {
    const project: Project = {
      settings: {
        data: {
          name: "No Project",
          projectId: "",
          projectUrl: new URL(API.apiAddress),
          sourcesUrl: new URL(API.apiAddress),
          lintUrl: new URL(API.apiAddress),
        },
        language: "auto",
        linter: "auto",
      },
      files: [],
      openFiles: [],
      activeFile: 0,
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
      //somehow no files were submitted? how is this even possible
      project.files = [
        {
          edited: false,
          unsaved: false,
          language: "auto",
          detectedLanguage: "txt",
          file: { name: "unnamed", path: "unnamed", content: "" },
        },
      ];
      project.openFiles = project.files;
      project.openFiles[0].id = 0;

      for (const state of project.openFiles) {
        state.id = this.internalFileId++;
      }
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
      project.openFiles = project.files.slice();

      //upload files to backend
      this.uploading = true;
      //extract file handles from file states
      let fileHandles: FileHandle[] = [];
      for (const fileState of project.files) {
        fileHandles.push(fileState.file);
      }
      const result = await this.uploadProject({
        name: event.projectName,
        files: fileHandles,
        language: "auto",
        linter: "auto",
      });

      if (result.errorMessage != undefined) {
        //I dislike having to do this again here when it's already been done in the function but can't think of anything better right now
        return;
      }

      project.settings.data = result;
      this.uploading = false;

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

  private async uploadProject(
    uploadData: SubmitProject
  ): Promise<ProjectResponse> {
    let result = await API.submitProject(uploadData);
    if (result.errorMessage != undefined) {
      console.log(result.errorMessage);
      //this.uploading = false;
      this.$emit("notification", {
        type: "error",
        message: result.errorMessage,
      });
    }
    return result;
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

  private async uploadFileChanges(event: FileChangeEvent): Promise<void> {
    let encounteredErrors = false;
    for (const state of event.openFiles) {
      let foundMatchingFile = false;
      for (const oldState of this.activeProjects[this.activeProject]
        .openFiles as FileState[]) {
        if (oldState.id == state.id) {
          foundMatchingFile = true;
          if (
            oldState.file.name == state.file.name &&
            oldState.file.path == state.file.path &&
            oldState.file.content == state.file.content
          ) {
            break;
          }
          const projectId =
            this.activeProjects[this.activeProject].settings.data.projectId;
          const result = await API.overwriteFile(projectId, state.file);
          if (!result.success) {
            this.passNotification({
              type: "error",
              message: result.errorMessage || "Unknown error",
            });
            encounteredErrors = true;
          }
          break;
        }
      }
      if (foundMatchingFile == false) {
        // went through all old files but didn't find an ID match, this must mean a new file; TODO add API new file endpoint
      }
    }

    this.activeProjects[this.activeProject].openFiles = event.openFiles;
    if (!encounteredErrors) {
      this.activeProjects[this.activeProject].files = event.files;
      (this.activeProjects[this.activeProject].openFiles as FileState[])[
        event.activeFile
      ].unsaved = false;
    }
  }

  private storeOpenFileChanges(event: OpenFileChangeEvent): void {
    this.activeProjects[this.activeProject].openFiles = event.openFiles;
    this.activeProjects[this.activeProject].activeFile = event.activeFile;
  }

  private setGetLintTries(): void {
    this.activeProjects[this.activeProject].remainingLintChecks = 3;
    this.activeProjects[this.activeProject].lintCheckTimer = setInterval(
      this.handleLintTimer,
      1000,
      this.activeProject
    );
  }

  private async handleLintTimer(projectIndex: number) {
    let remainingChecks = 5;
    if (this.activeProjects[projectIndex].remainingLintChecks != undefined) {
      remainingChecks = this.activeProjects[projectIndex]
        .remainingLintChecks as number;
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
