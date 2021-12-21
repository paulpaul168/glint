import { FileHandle } from "@/components/types/interfaces";

export interface SubmitProject {
  name: string;
  files: FileHandle[];
  language: string;
  linter: string;
}
