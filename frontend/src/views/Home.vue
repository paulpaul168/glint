<template>
  <div class="d-flex flex-row main-pane">
    <div class="project-list">
      <project-list
        :projects="activeProjects"
        :activeProject="activeProject"
        :fetchingProjects="downloading"
        @set-active-project="activeProject = $event"
        @linter-set="passLinter"
        @notification="passNotification"
        @create-project="createEmptyProject"
        @refresh-projects="loadProjects"
        @toggle-project-info="toggleProjectView"
        @open-file="openFile($event)"
        @delete-project="deleteActiveProject"
        @close-project="closeActiveProject"
        @set-patterns="searchPatterns = $event"
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
        @rename-file="handleFileRename($event)"
        @retry-get-lint="setGetLintTries"
        @request-new-lint="requestNewLint"
        @create-project-event="fillProject($event)"
      />
    </div>
    <global-notifier :notification="notification"></global-notifier>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";

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
  SearchPatterns,
  SearchResult,
} from "@/components/types/interfaces";
import { getLanguage } from "@/services/LanguageDetection";
import { SubmitProject } from "@/services/types/api_requests_interfaces";
import {
  LintResponse,
  ProjectDataResponse,
  ProjectListResponse,
  ProjectResponse,
} from "@/services/types/api_responses_interfaces";
import { Dictionary } from "vue-router/types/router";

@Component({
  components: {
    ContentView,
    ProjectList,
    GlobalNotifier,
  },
})
export default class Home extends Vue {
  name = "Home";

  private downloading = false;
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
  ];
  private internalFileId = 0;
  private internalProjectId = 0;

  private searchPatterns: SearchPatterns = {};
  private searchResults: Dictionary<SearchResult[]> = {};

  private linter = "auto";

  created(): void {
    this.loadProjects();
  }

  @Watch("activeProject")
  @Watch("searchPatterns")
  searchFiles(): void {
    //TODO add some sort of buffering or project specific storage to not have to re-find all the matches
    this.searchResults = {};
    for (const project of this.activeProjects) {
      for (const state of project.files) {
        this.searchResults[state.file.path] = [];
        for (const [, pattern] of Object.entries(this.searchPatterns)) {
          const regex = new RegExp(
            pattern.regex
              .replaceAll("\\", "\\\\")
              .substring(1, pattern.regex.lastIndexOf("/")),
            "g" +
              pattern.regex
                .substring(pattern.regex.lastIndexOf("/") + 1)
                .replace("g", "")
          );
          const matches = [...state.file.content.matchAll(regex)];
          for (const match of matches) {
            if (match.index != undefined) {
              const lineStartPos =
                this.getLineStartPos(state.file.content, match.index) + 1;
              let lineEnd = state.file.content.indexOf("\n", lineStartPos);
              lineEnd = lineEnd == -1 ? state.file.content.length : lineEnd;
              console.log("line pos:", lineStartPos, lineEnd);
              const result: SearchResult = {
                query: pattern.regex,
                snippet: state.file.content.substring(lineStartPos, lineEnd),
                source: state.file,
                line: this.getLineNumberFromPos(
                  state.file.content,
                  match.index
                ),
              };
              this.searchResults[state.file.path].push(result);
            }
          }
        }
      }
    }
  }

  private toggleProjectView(): void {
    const viewMode = this.activeProjects[this.activeProject].viewMode;
    if (viewMode == "files") {
      this.activeProjects[this.activeProject].viewMode = "overview";
    } else if (viewMode == "overview") {
      this.activeProjects[this.activeProject].viewMode = "files";
    } else {
      //should never be needed, but if there's an error we return to a known state
      this.activeProjects[this.activeProject].viewMode = "files";
    }
  }

  private getLineNumberFromPos(fileContent: string, pos: number): number {
    let line = 0;
    const regex = /(^)[\S\s]/gm;
    let match = regex.exec(fileContent);
    while (match != null) {
      if (match.index > pos) {
        break;
      }
      line++;
      match = regex.exec(fileContent);
    }
    return line;
  }

  private getLineStartPos(fileContent: string, pos: number): number {
    const index = fileContent.substring(0, pos).lastIndexOf("\n");
    return index == -1 ? 0 : index;
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
        } else if (index == this.activeProject) {
          this.passNotification({
            type: "info",
            message: "You are already in an empty project.",
            timeout: 2000,
          });
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
    this.downloading = true;
    const respProjects: ProjectListResponse = await API.getProjects();
    if (respProjects.errorMessage != undefined) {
      console.log(respProjects.errorMessage);
      this.passNotification({
        type: "error",
        message: respProjects.errorMessage,
      });
      this.downloading = false;
      return;
    }

    let newProjectList: Project[] = [];
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
        this.downloading = false;
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

      const lintData: LintResponse = await API.getLint(project.projectId);
      newProjectList.push(
        this.createProjectFromResponse(project, respData, lintData)
      );
    }
    if (newProjectList.length > 0) {
      if (this.activeProject >= newProjectList.length) {
        this.activeProject = 0;
      }
      this.activeProjects = newProjectList;
    }
    this.downloading = false;
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
      const fileToOpen: FileState = {
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
          //have to individually copy because otherwise I get a reference which breaks stuff
          //the stupid thing with the slice is needed so it actually strcpy and not just references the strings
          //I need files and openFiles to be separate copies that can be separately edited
          fileToOpen.file.name = (" " + state.file.name).slice(1);
          fileToOpen.file.path = (" " + state.file.path).slice(1);
          fileToOpen.file.content = (" " + state.file.content).slice(1);
          fileToOpen.language = (" " + state.language).slice(1);
          fileToOpen.detectedLanguage = (" " + state.detectedLanguage).slice(1);
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
    projectData: ProjectDataResponse,
    lintData: LintResponse
  ): Project {
    const returnProject: Project = {
      settings: {
        data: {
          name: project.name,
          projectId: project.projectId,
          projectUrl: project.projectUrl,
          sourcesUrl: project.sourcesUrl,
          lintUrl: project.lintUrl,
        },
        linters: {},
      },
      files: [],
      openFiles: [],
      activeFile: 0,
      lintData: lintData, //TODO if this can't be fetched here there is no way (short of editing and saving a file) to get to lint results later on.
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
      bufferProject.openFiles = bufferProject.files.slice();
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
      //bufferProject.openFiles = bufferProject.files.slice();

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

  private closeActiveProject(): void {
    const projectToClose = this.activeProject;
    if (this.activeProject > 0) {
      this.activeProject--;
    }
    this.activeProjects.splice(projectToClose, 1);
    //set up a new empty project if it's the last project that was closed
    if (this.activeProjects.length == 0) {
      this.createEmptyProject();
    }
  }

  private async deleteActiveProject(): Promise<void> {
    const projectToDelete = this.activeProject; //buffer this in case deletion takes some time and user switches active project in that time
    //delete from backend
    let result = await API.deleteProject(
      this.activeProjects[projectToDelete].settings.data.projectId
    );

    //if deletion failed, don't remove it from the UI and return with error
    if (result.errorMessage != undefined) {
      console.log(result.errorMessage);
      this.passNotification({
        type: "error",
        message: result.errorMessage,
      });
      return;
    }

    //remove from UI if deletion succeeded
    this.closeActiveProject();
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
      console.log("compare state", state.file.name);
      let foundMatchingFile = false;
      for (const oldState of this.activeProjects[this.activeProject].files) {
        console.log("old state", oldState.file.name);
        if (oldState.id == state.id) {
          foundMatchingFile = true;
          console.log("ids match!");
          if (
            oldState.file.name == state.file.name &&
            oldState.file.path == state.file.path &&
            oldState.file.content == state.file.content
          ) {
            console.log("content is identical");
            //console.log(oldState.file.content, "---", state.file.content);
            break;
          }
          console.log("writing file");
          const projectId =
            this.activeProjects[this.activeProject].settings.data.projectId;
          let oldFilePath: string | undefined = undefined;
          if (oldState.file.name != state.file.name) {
            //file got renamed
            oldFilePath = oldState.file.path;
          }
          const result = await API.overwriteFile(
            projectId,
            state.file,
            oldFilePath
          );
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
        console.log("found no matching file");
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

  private async handleFileRename(event: OpenFileChangeEvent): Promise<void> {
    this.activeProjects[this.activeProject].files.forEach((state, index) => {
      //go through all files to update the renamed one in the list
      if (
        state.file.path ==
        this.activeProjects[this.activeProject].openFiles?.[event.activeFile]
          .file.path
      ) {
        //if the file paths match, update name and path
        this.activeProjects[this.activeProject].files[index].file.name =
          event.openFiles[event.activeFile].file.name;
        this.activeProjects[this.activeProject].files[index].file.path =
          event.openFiles[event.activeFile].file.path;
      }
    });

    (this.activeProjects[this.activeProject].openFiles as FileState[])[
      event.activeFile
    ].file.name = (" " + event.openFiles[event.activeFile].file.name).slice(1);
    (this.activeProjects[this.activeProject].openFiles as FileState[])[
      event.activeFile
    ].file.path = (" " + event.openFiles[event.activeFile].file.path).slice(1);
  }

  private setGetLintTries(): void {
    this.activeProjects[this.activeProject].remainingLintChecks = 3;
    this.activeProjects[this.activeProject].lintData.status = "processing";
    this.activeProjects[this.activeProject].lintCheckTimer = setInterval(
      this.handleLintTimer,
      1000,
      this.activeProject
    );
  }

  private requestNewLint(): void {
    API.editProject(
      this.activeProjects[this.activeProject].settings.data.projectId,
      {
        name: null,
        linters: null,
      }
    );
    this.setGetLintTries();
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
}

.main-content-pane {
  height: 100%;
}

.project-list {
  max-width: 400px;
  min-width: 250px;
  width: fit-content;
  /*min-width: 200px; the automatic content based resizing doesn't quite work, fixed size is better for now*/
  flex: 0 0 content;
}

.content-view {
  flex-grow: 100;
  padding-left: 12px;
}
</style>
