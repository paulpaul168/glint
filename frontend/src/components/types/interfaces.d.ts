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
  files: FileHandle[];
}

export interface LintEvent {
  status: string;
  linter: string;
  lintFiles: [
    {
      name: string;
      path: string;
      lints: Lint[];
    }
  ];
}

export interface FileState {
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
  url?: string; //not sure if this should be optional or always defaulted to empty string
}
