import { FileHandle } from "@/components/types/interfaces";

export interface SubmitProject {
  name: string;
  files: FileHandle[];
  linters: LinterMapping;
}
