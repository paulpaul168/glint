export interface Events {
  file: FileEvent;
}

export interface FileHandle {
  name: string;
  path: string;
  content: string;
}

export interface FileEvent {
  files: FileHandle[];
}

export interface FileState {
  file: FileHandle;
  unsaved: boolean;
  edited: boolean;
}
