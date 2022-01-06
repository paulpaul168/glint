export interface Events {
  files: CreateProjectEvent;
  lints: LintEvent;
  notifs: Notification;
  fileChange: FileChangeEvent;
  openFileChange: OpenFileChangeEvent;
  goToFile: GoToFileEvent;
}

export interface Notification {
  type: string;
  message: string;
  timeout?: number;
}

export interface FileChangeEvent {
  files: FileState[];
  openFiles: FileState[];
  activeFile: number;
}

export interface OpenFileChangeEvent {
  openFiles: FileState[];
  activeFile: number;
}

export interface CreateProjectEvent {
  projectName: string;
  files: FileHandle[];
  error?: unknown;
}

export interface GoToFileEvent {
  filePath: string;
  line: number;
}

export interface FileHandle {
  name: string;
  path: string;
  content: string;
}

export interface FileState {
  id?: number;
  language: string;
  detectedLanguage: string;
  file: FileHandle;
  unsaved: boolean;
  edited: boolean;
}

export interface LinterMapping {
  [language: string]: string;
}

export interface Lint {
  fileName?: string; //a bit superfluous for the lintview, but needed in the lintcard to generate the link to the file

  line: number;
  endLine: number;
  column: number;
  endColumn: number;

  header: string;
  message: string;
  url?: URL; //not sure if this should be optional or always defaulted to empty string
}

export interface Project {
  settings: ProjectData;
  files: FileState[];
  openFiles?: FileState[];
  activeFile?: number;
  lintData: LintResponse;
  lintCheckTimer?: number;
  remainingLintChecks?: number;
  viewMode?: string; //which state the UI is in, can be "files" = depending on files, either shows source, lint or uploader, "project" = show project overview
}

export interface ProjectData {
  data: ProjectResponse;
  linters: LinterMapping;
}

export interface SearchPattern {
  name: string;
  regex: string;
}

export interface SearchPatterns {
  [id: string]: SearchPattern;
}

export interface SearchResult {
  patternId: string;
  snippet: string;
  source: FileHandle;
  line: number;
}
