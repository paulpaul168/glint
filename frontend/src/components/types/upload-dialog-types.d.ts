export interface Events {
  file: FileEvent;
}

export interface FileHandle {
  name: string;
  content: string;
}

export interface FileEvent {
  files: FileHandle[];
}
