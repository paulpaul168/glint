<template>
  <div class="d-flex flex-row main-pane">
    <div class="project-list">
      <project-list
        :projects="activeProjects"
        :activeProject="activeProject"
        @set-active-project="activeProject = $event"
        @linter-set="passLinter"
        @notification="passNotification"
        @create-project="createEmptyProject"
        @open-file="openFile($event)"
      />
    </div>
    <div class="content-view">
      <content-view
        :project="activeProjects[activeProject]"
        :uploading="false"
        ref="contentView"
        @notification="passNotification"
        @files-change="uploadFileChanges"
        @open-files-change="storeOpenFileChanges"
        @retry-get-lint="setGetLintTries"
        @create-project-event="fillProject($event)"
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
import {
  ProjectDataResponse,
  ProjectListResponse,
  ProjectResponse,
} from "@/services/types/api_responses_interfaces";

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
          projectId: "",
          projectUrl: new URL(API.apiAddress),
          sourcesUrl: new URL(API.apiAddress),
          lintUrl: new URL(API.apiAddress),
        },
        linters: {},
      },
      files: [],
      openFiles: [],
      activeFile: 0,
      lintData: {
        status: "",
        linters: {},
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
  private internalProjectId = 0;

  private linter = "auto";

  created(): void {
    this.loadProjects();
  }

  private createEmptyProject(): void {
    const emptyProject: Project = {
      settings: {
        data: {
          name: "New Project",
          projectId: "",
          projectUrl: new URL(API.apiAddress),
          sourcesUrl: new URL(API.apiAddress),
          lintUrl: new URL(API.apiAddress),
        },
        linters: {},
      },
      files: [],
      openFiles: [],
      activeFile: 0,
      lintData: {
        status: "",
        linters: {},
        lintFiles: [],
      },
      viewMode: "files",
      remainingLintChecks: 5,
    };

    let foundEmpty = false;
    console.log("active", this.activeProject);
    this.activeProjects.forEach((project, index) => {
      if (project.settings.data.projectId == "") {
        if (index != this.activeProject) {
          this.passNotification({
            type: "info",
            message:
              "Switching to existing empty project instead of creating another one.",
            timeout: 2000,
          });
          this.activeProject = index;
        }
        foundEmpty = true;
      }
    });

    if (!foundEmpty) {
      this.activeProjects.push(emptyProject);
      this.activeProject = this.activeProjects.length - 1;
    }
  }

  private async loadProjects(): Promise<void> {
    const respProjects: ProjectListResponse = await API.getProjects();
    if (respProjects.errorMessage != undefined) {
      console.log(respProjects.errorMessage);
      this.passNotification({
        type: "error",
        message: respProjects.errorMessage,
      });
      return;
    }

    let newProjectList: Project[] = [];
    console.log(
      "projects:",
      respProjects.projects[0].name,
      respProjects.projects[0].projectId
    );
    for (const project of respProjects.projects) {
      if (project.projectId == "" || project.projectId == undefined) {
        console.log(
          "Encountered empty or undefined project ID after fetching project data"
        );
        this.passNotification({
          type: "error",
          message:
            "Encountered empty or undefined project ID after fetching project data",
        });
        return;
      }
      const respData: ProjectDataResponse = await API.getProjectData(
        project.projectId
      );
      if (respData.errorMessage != undefined) {
        console.log(respData.errorMessage);
        this.passNotification({
          type: "error",
          message: respData.errorMessage,
        });
      }
      newProjectList.push(this.createProjectFromResponse(project, respData));
    }
    this.activeProjects = newProjectList;
  }

  private openFile(path: string): void {
    let isAlreadyOpen = false;
    this.activeProjects[this.activeProject].openFiles?.forEach(
      (state, index) => {
        if (state.file.path == path) {
          this.activeProjects[this.activeProject].activeFile = index;
          isAlreadyOpen = true;
          return;
        }
      }
    );
    if (!isAlreadyOpen) {
      let fileToOpen: FileState = {
        file: {
          name: "",
          path: "",
          content: "",
        },
        language: "auto",
        detectedLanguage: "",
        unsaved: false,
        edited: false,
      };
      let fileFound = false;
      for (const state of this.activeProjects[this.activeProject].files) {
        if (state.file.path == path) {
          fileToOpen = state;
          fileFound = true;
          break;
        }
      }
      if (fileFound) {
        this.activeProjects[this.activeProject].openFiles?.push(fileToOpen);
        this.activeProjects[this.activeProject].activeFile =
          (this.activeProjects[this.activeProject].openFiles
            ?.length as number) - 1;
      } else {
        this.passNotification({
          type: "error",
          message: "Tried opening file, but couldn't find file with right path",
        });
      }
    }
  }

  private createProjectFromResponse(
    project: ProjectResponse,
    projectData: ProjectDataResponse
  ): Project {
    const returnProject: Project = {
      settings: {
        data: {
          name: project.name,
          projectId: project.projectId,
          projectUrl: new URL(project.projectUrl),
          sourcesUrl: new URL(project.sourcesUrl),
          lintUrl: new URL(project.lintUrl),
        },
        linters: {},
      },
      files: [],
      openFiles: [],
      activeFile: 0,
      lintData: {
        status: "",
        linters: {},
        lintFiles: [],
      },
      viewMode: "files",
      remainingLintChecks: 5,
    };

    for (const file of projectData.files as FileHandle[]) {
      //why is is seen as "any" without me casting to filehandle[]? it's defined as filehandle[] in the interface
      returnProject.files.push({
        file: file,
        language: "auto",
        detectedLanguage: getLanguage(file.name),
        unsaved: false,
        edited: false,
      });
    }

    return returnProject;
  }

  private async fillProject(event: CreateProjectEvent): Promise<void> {
    this.createEmptyProject(); //either create or switch to a suitable empty project
    const bufferProject: Project = this.activeProjects[this.activeProject];

    //get files from user file event and show it in UI
    if (event.files.length == 0) {
      //somehow no files were submitted? how is this even possible
      bufferProject.files = [
        {
          edited: false,
          unsaved: false,
          language: "auto",
          detectedLanguage: "txt",
          file: { name: "unnamed", path: "unnamed", content: "" },
        },
      ];
      bufferProject.openFiles = bufferProject.files;
      (bufferProject.openFiles as FileState[])[0].id = 0;

      for (const state of bufferProject.openFiles as FileState[]) {
        state.id = this.internalFileId++;
      }
    } else {
      bufferProject.files = [];
      for (let file of event.files) {
        bufferProject.files.push({
          edited: false,
          unsaved: false,
          language: "auto",
          detectedLanguage: getLanguage(file.name),
          file: file,
        });
      }
      bufferProject.openFiles = bufferProject.files.slice();

      //upload files to backend
      this.uploading = true;
      //extract file handles from file states
      let fileHandles: FileHandle[] = [];
      for (const fileState of bufferProject.files) {
        fileHandles.push(fileState.file);
      }
      const result = await this.uploadProject({
        name: event.projectName,
        files: fileHandles,
        linters: {},
      });

      if (result.errorMessage != undefined) {
        //I dislike having to do this again here when it's already been done in the function but can't think of anything better right now
        return;
      }

      bufferProject.settings.data = result;
      //bufferProject.settings.data.projectId = String(this.internalProjectId++);
      this.uploading = false;

      //set interval for asking for lint status every second. handler has to deactivate asking for lint results on receiving results (or an error)
      bufferProject.lintData.status = "processing";
      bufferProject.lintCheckTimer = setInterval(
        this.handleLintTimer,
        1000,
        this.activeProject
      );
      this.activeProjects[this.activeProject] = bufferProject;
      (this.$refs["contentView"] as ContentView).projectChanged(); //this is a horrible fix and I don't know why I need it, the project watcher should see this. maybe because the original bufferproject is from the same list thus not changing the reference?
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
