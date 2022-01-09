import { FileHandle, LinterMapping } from "@/components/types/interfaces";

export interface SubmitProject {
  name: string;
  files?: FileHandle[];
  zip?: string;
  linters: LinterMapping;
}

export interface EditProject {
  name: string | null;
  linters: LinterMapping | null;
}

export interface SearchPatternRequest {
  patternName: string;
  regex: string;
}
