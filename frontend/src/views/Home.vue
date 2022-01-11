<template>
  <div class="d-flex flex-row main-pane">
    <div class="project-list">
      <project-list
        :projects="activeProjects"
        :activeProject="activeProject"
        :fetchingProjects="downloading"
        @set-active-project="setActiveProject($event)"
        @linter-set="passLinter"
        @notification="passNotification"
        @create-project="createEmptyProject"
        @refresh-projects="loadProjects"
        @toggle-project-info="toggleProjectView"
        @upload-files="addFile($event)"
        @open-file="openFile($event)"
        @delete-file="deleteFile($event)"
        @rename-project="renameActiveProject($event)"
        @delete-project="deleteActiveProject"
        @close-project="closeActiveProject"
        @set-patterns="searchPatterns = $event"
        @set-linter-mappings="setLinters"
      />
    </div>
    <div class="content-view">
      <content-view
        :project="activeProjects[activeProject]"
        :uploading="false"
        :searchPatterns="searchPatterns"
        :searchResults="
          searchResults[activeProjects[activeProject].settings.data.projectId]
        "
        ref="contentView"
        @notification="passNotification"
        @files-change="uploadFileChanges"
        @open-file="openFile($event)"
        @open-files-change="storeOpenFileChanges"
        @rename-file="handleFileRename($event)"
        @files-view-change="
          activeProjects[activeProject].filesViewMode = $event
        "
        @retry-get-lint="setGetLintTries"
        @request-new-lint="requestNewLint"
        @create-project-event="fillProject($event)"
        @create-project-zip-event="uploadProjectZip($event)"
        @close-project-overview="toggleProjectView"
        @start-secret-search="searchFiles"
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
  AddFileEvent,
  CreateProjectEvent,
  CreateProjectZipEvent,
  FileChangeEvent,
  FileHandle,
  FileState,
  GoToFileEvent,
  LinterMapping,
  Notification,
  OpenFileChangeEvent,
  Project,
  SearchPatterns,
  SearchResult,
} from "@/components/types/interfaces";
import { getLanguage } from "@/services/LanguageDetection";
import { SubmitProject } from "@/services/types/api_requests_interfaces";
import {
  GenericStatusResponse,
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
      contentViewMode: "files",
      filesViewMode: "auto",
      remainingLintChecks: 5,
    },
  ];
  private internalFileId = 0;
  private internalProjectId = 0;

  private searchPatterns: SearchPatterns = {};
  //a dict of projects containing a dict of files
  private searchResults: Dictionary<Dictionary<SearchResult[]>> = {};

  private linter = "auto";

  created(): void {
    this.loadProjects(this.parseUrlParams);
  }

  private parseUrlParams(): void {
    if (
      this.$route.query.project != undefined &&
      this.$route.query.project != ""
    ) {
      //if project is defined in URL, parse it and try to set the project
      let foundProject = false;
      this.activeProjects.forEach((project, index) => {
        if (
          project.settings.data.projectId ==
          decodeURIComponent(this.$route.query.project as string)
        ) {
          this.activeProject = index;
          foundProject = true;
          return;
        }
      });

      if (foundProject) {
        if (this.$route.query.file != undefined) {
          this.openFile({
            filePath: decodeURIComponent(this.$route.query.file as string),
          });
        }
      } else {
        this.updateUrlParams(null);
      }
    } else {
      this.updateUrlParams(null);
    }
  }

  private updateUrlParams(projectId: string | null, filePath?: string): void {
    let query = {};
    if (projectId != null && projectId != "") {
      if (filePath != undefined) {
        query = {
          project: encodeURIComponent(projectId),
          file: encodeURIComponent(filePath),
        };
      } else {
        query = { project: projectId };
      }
    }
    if (
      this.$route.path == "/" &&
      JSON.stringify(this.$route.query) == JSON.stringify(query)
    ) {
      //if the new location is the same old location, return, the rest would be unnecessary
      return;
    }
    this.$router.push({
      path: "/",
      query: query,
    });
  }

  @Watch("activeProject")
  @Watch("searchPatterns")
  searchFiles(): void {
    //TODO add some sort of buffering or project specific storage to not have to re-find all the matches
    this.searchResults = {};
    for (const project of this.activeProjects) {
      const projectId = project.settings.data.projectId;
      this.searchResults[projectId] = {};
      for (const state of project.files) {
        this.searchResults[projectId][state.file.path] = [];
        for (const [id, pattern] of Object.entries(this.searchPatterns)) {
          const regex = new RegExp(
            pattern.regex.substring(1, pattern.regex.lastIndexOf("/")),
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
              const result: SearchResult = {
                patternId: id,
                snippet: state.file.content.substring(lineStartPos, lineEnd),
                source: state.file,
                line: this.getLineNumberFromPos(
                  state.file.content,
                  match.index
                ),
                col: match.index - lineStartPos,
              };
              this.searchResults[projectId][state.file.path].push(result);
            }
          }
        }
      }
    }
  }

  private toggleProjectView(): void {
    const contentViewMode =
      this.activeProjects[this.activeProject].contentViewMode;
    if (contentViewMode == "files") {
      this.activeProjects[this.activeProject].contentViewMode = "overview";
    } else if (contentViewMode == "overview") {
      this.activeProjects[this.activeProject].contentViewMode = "files";
    } else {
      //should never be needed, but if there's an error we return to a known state
      this.activeProjects[this.activeProject].contentViewMode = "files";
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
      contentViewMode: "files",
      filesViewMode: "auto",
      remainingLintChecks: 10,
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
          //this triggers in a normal usecase as well, need to either change the testing or just leave it out
          /*this.passNotification({
            type: "info",
            message: "You are already in an empty project.",
            timeout: 2000,
          });*/
        }
        foundEmpty = true;
      }
    });

    if (!foundEmpty) {
      this.activeProjects.push(emptyProject);
      this.activeProject = this.activeProjects.length - 1;
    }
  }

  private async loadProjects(callback?: () => void): Promise<void> {
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
    this.activeProjects.forEach((project, index) => {
      if (project.lintData.status == "processing") {
        this.setGetLintTries(index);
      }
    });
    callback?.();
  }

  private setLinters(linters: LinterMapping): void {
    this.activeProjects[this.activeProject].settings.linters = linters;
  }

  //TODO: GoToFileEvent sounds weird for this, but it contains the needed data. consider renaming?
  private async deleteFile(data: GoToFileEvent): Promise<void> {
    let projectId = "";
    if (data.projectId != undefined) {
      projectId = data.projectId;
    } else {
      projectId =
        this.activeProjects[this.activeProject].settings.data.projectId;
    }
    const result: GenericStatusResponse = await API.deleteFile(
      projectId,
      data.filePath
    );

    if (result.errorMessage != undefined) {
      console.log(result.errorMessage);
      this.passNotification({
        type: "error",
        message: result.errorMessage,
      });
      return;
    }

    //TODO this is awful and I hate it, but it's the quickest way to make sure that
    //the project list is properly synced with no errors. I can't go through various error states
    //and check how to gracefully get out of them, it takes too long and the deadline is too close
    this.loadProjects();
  }

  private setActiveProject(projectIndex: number): void {
    this.activeProject = projectIndex;
    this.updateUrlParams(
      this.activeProjects[projectIndex].settings.data.projectId
    );
  }

  private openFile(data: GoToFileEvent): void {
    if (data.projectId != undefined) {
      //if a projectId is set, switch to that project
      if (
        this.activeProjects[this.activeProject].settings.data.projectId !=
        data.projectId
      ) {
        //but only if we aren't already in that project
        this.activeProjects.forEach((project, index) => {
          if (project.settings.data.projectId == data.projectId) {
            this.activeProject = index;
            return;
          }
        });
      }
    }

    let isAlreadyOpen = false;
    this.activeProjects[this.activeProject].openFiles?.forEach(
      (state, index) => {
        if (state.file.path == data.filePath) {
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
        id: -1,
      };
      let fileFound = false;
      for (const state of this.activeProjects[this.activeProject].files) {
        if (state.file.path == data.filePath) {
          //have to individually copy because otherwise I get a reference which breaks stuff
          //the stupid thing with the slice is needed so it actually strcpy and not just references the strings
          //I need files and openFiles to be separate copies that can be separately edited
          fileToOpen.file.name = (" " + state.file.name).slice(1);
          fileToOpen.file.path = (" " + state.file.path).slice(1);
          fileToOpen.file.content = (" " + state.file.content).slice(1);
          fileToOpen.language = (" " + state.language).slice(1);
          fileToOpen.detectedLanguage = (" " + state.detectedLanguage).slice(1);
          fileToOpen.id = state.id;
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
    this.activeProjects[this.activeProject].contentViewMode = "files";
    this.activeProjects[this.activeProject].filesViewMode = "source";
    if (data.line != undefined) {
      this.$nextTick(() => {
        (this.$refs.contentView as ContentView).scrollTo(data.line || 0);
      });
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
        linters: projectData.linters,
      },
      files: [],
      openFiles: [],
      activeFile: 0,
      lintData: lintData, //TODO if this can't be fetched here there is no way (short of editing and saving a file) to get to lint results later on.
      contentViewMode: "files",
      filesViewMode: "auto",
      remainingLintChecks: 5,
    };

    for (const file of projectData.files as FileHandle[]) {
      //why is this seen as "any" without me casting to filehandle[]? it's defined as filehandle[] in the interface
      returnProject.files.push({
        file: file,
        language: "auto",
        detectedLanguage: getLanguage(file.name),
        unsaved: false,
        edited: false,
        id: this.internalFileId++,
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
    } else {
      bufferProject.files = [];
      for (let file of event.files) {
        bufferProject.files.push({
          edited: false,
          unsaved: false,
          language: "auto",
          detectedLanguage: getLanguage(file.name),
          file: file,
          id: this.internalFileId++,
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
        this.passNotification({
          type: "error",
          message: result.errorMessage,
        });
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
      this.updateUrlParams(bufferProject.settings.data.projectId);
    }
  }

  private async uploadProjectZip(data: CreateProjectZipEvent): Promise<void> {
    const result = await API.submitProject({
      name: data.projectName,
      zip: data.zip,
      linters: {},
    });

    if (result.errorMessage != undefined) {
      this.passNotification({
        type: "error",
        message: result.errorMessage,
      });
      return;
    }
    this.loadProjects();
  }

  private async renameActiveProject(newName: string): Promise<void> {
    const result = await API.editProject(
      this.activeProjects[this.activeProject].settings.data.projectId,
      {
        name: newName,
        linters: null,
      }
    );

    //if rename failed, don't rename it in UI and return with error
    if (result.errorMessage != undefined) {
      console.log(result.errorMessage);
      this.passNotification({
        type: "error",
        message: result.errorMessage,
      });
      return;
    }

    //if rename succeeded, actually rename the UI element and internal data
    this.activeProjects[this.activeProject].settings.data.name = newName;
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
    const result = await API.deleteProject(
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

    //remove project reference from URL
    this.updateUrlParams(null);
  }

  private async uploadProject(
    uploadData: SubmitProject
  ): Promise<ProjectResponse> {
    let result = await API.submitProject(uploadData);
    if (result.errorMessage != undefined) {
      console.log(result.errorMessage);
      //this.uploading = false;
      this.passNotification({
        type: "error",
        message: result.errorMessage,
      });
    }
    return result;
  }

  private async addFile(event: AddFileEvent): Promise<void> {
    await this.uploadFileChanges({
      files: event.files,
      openFiles: event.files,
      activeFile: 0,
    });
  }

  private async uploadFileChanges(event: FileChangeEvent): Promise<void> {
    let encounteredErrors = false;
    let foundMatchingFile = false;
    for (const state of event.openFiles) {
      for (const oldState of this.activeProjects[this.activeProject].files) {
        if (oldState.id == state.id) {
          //TODO If I ever rewrite this, a lot of headache could be removed by simply
          //not sending all files in the internal events. why was I so stupid
          foundMatchingFile = true;
          if (
            oldState.file.name == state.file.name &&
            oldState.file.path == state.file.path &&
            oldState.file.content == state.file.content
          ) {
            //console.log(oldState.file.content, "---", state.file.content);
            //console.log("identical file");
            //console.log(oldState.file.path, state.file.path);
            break;
          }
          //console.log("writing file");
          const projectId =
            this.activeProjects[this.activeProject].settings.data.projectId;
          let oldFilePath: string | undefined = undefined;
          if (oldState.file.name != state.file.name) {
            //file got renamed
            oldFilePath = oldState.file.path;
            //console.log("rename", oldFilePath);
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
        for (const state of event.files) {
          const projectId =
            this.activeProjects[this.activeProject].settings.data.projectId;
          const result = await API.addFile(projectId, state.file);
          if (result.errorMessage != undefined) {
            this.passNotification({
              type: "error",
              message: result.errorMessage || "Unknown error",
            });
            encounteredErrors = true;
          }
        }
      }
    }

    this.activeProjects[this.activeProject].openFiles = event.openFiles;
    if (!encounteredErrors) {
      if (foundMatchingFile) {
        this.activeProjects[this.activeProject].files = event.files;
        (this.activeProjects[this.activeProject].openFiles as FileState[])[
          event.activeFile
        ].unsaved = false;
      } else {
        this.activeProjects[this.activeProject].files = this.activeProjects[
          this.activeProject
        ].files.concat(event.files);
      }
    }
  }

  private storeOpenFileChanges(event: OpenFileChangeEvent): void {
    if (
      event.activeFile == undefined ||
      event.activeFile >= event.openFiles.length
    ) {
      this.updateUrlParams(
        this.activeProjects[this.activeProject].settings.data.projectId
      );
    } else {
      this.updateUrlParams(
        this.activeProjects[this.activeProject].settings.data.projectId,
        event.openFiles[event.activeFile].file.path
      );
    }
    this.activeProjects[this.activeProject].openFiles = event.openFiles;
    this.activeProjects[this.activeProject].activeFile = event.activeFile;
  }

  private async handleFileRename(event: OpenFileChangeEvent): Promise<void> {
    //console.log("renaming", event.openFiles[event.activeFile].file.path);
    this.activeProjects[this.activeProject].files.forEach(
      async (state, index) => {
        //go through all files to update the renamed one in the list
        if (state.id == event.openFiles[event.activeFile].id) {
          //if the file paths match, update file name and path on backend and then UI
          await this.uploadFileChanges({
            files: this.activeProjects[this.activeProject].files,
            openFiles: event.openFiles,
            activeFile: event.activeFile,
          });
          //console.log("updating UI", event.openFiles[event.activeFile].file.name);
          this.activeProjects[this.activeProject].files[index].file.name =
            event.openFiles[event.activeFile].file.name;
          this.activeProjects[this.activeProject].files[index].file.path =
            event.openFiles[event.activeFile].file.path;
        }
      }
    );

    (this.activeProjects[this.activeProject].openFiles as FileState[])[
      event.activeFile
    ].file.name = (" " + event.openFiles[event.activeFile].file.name).slice(1);
    (this.activeProjects[this.activeProject].openFiles as FileState[])[
      event.activeFile
    ].file.path = (" " + event.openFiles[event.activeFile].file.path).slice(1);
  }

  private setGetLintTries(projectIndex: number): void {
    this.activeProjects[projectIndex].remainingLintChecks = 10;
    this.activeProjects[projectIndex].lintData.status = "processing";
    this.activeProjects[projectIndex].lintCheckTimer = setInterval(
      this.handleLintTimer,
      1000,
      projectIndex
    );
  }

  private requestNewLint(): void {
    API.editProject(
      this.activeProjects[this.activeProject].settings.data.projectId,
      {
        name: null,
        linters: this.activeProjects[this.activeProject].settings.linters,
      }
    );
    this.setGetLintTries(this.activeProject);
  }

  private async handleLintTimer(projectIndex: number) {
    let remainingChecks = 10;
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
          let errorMessage =
            this.activeProjects[projectIndex].lintData.errorMessage;
          if (this.activeProjects[projectIndex].lintData.status != "error") {
            //if no generic error message is set (by my own backend API code) the error came from
            //the backend and should be displayed
            errorMessage = this.activeProjects[projectIndex].lintData.status;
            //TODO this code feels *very* fragile, I really dislike that, should probably be handled in the backend API instead
          }
          this.passNotification({
            type: "error",
            message: errorMessage,
          });
        }
      }
    } else {
      clearInterval(this.activeProjects[projectIndex].lintCheckTimer);
      this.passNotification({
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
  max-width: 600px;
  min-width: 250px;
  width: fit-content;
  /*min-width: 200px; the automatic content based resizing doesn't quite work, fixed size is better for now*/
  flex: 0 0 content;
}

.content-view {
  flex-grow: 100;
}
</style>
