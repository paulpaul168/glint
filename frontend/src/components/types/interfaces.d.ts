import { ProjectResponse } from "@/services/types/api_responses_interfaces";

export interface Events {
  files: FileEvent;
  lints: LintEvent;
}

export interface FileHandle {
  name: string;
  path: string;
  content: string;
}

export interface FileEvent {
  projectName: string;
  files: FileHandle[];
  error?: unknown;
}

export interface FileState {
  id?: number;
  file: FileHandle;
  unsaved: boolean;
  edited: boolean;
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
  data: ProjectData;
  files: FileState[];
}

export interface ProjectData {
  project: ProjectResponse;
  language: string;
  linter: string;
}
