import { LinterMapping, SearchPattern } from "@/components/types/interfaces";

export interface ProjectListResponse {
  projects: ProjectResponse[];
  errorMessage?: string;
}

export interface ProjectResponse {
  name: string;
  projectId: string;
  projectUrl: URL;
  sourcesUrl: URL;
  lintUrl: URL;
  errorMessage?: string;
}

export interface ProjectDataResponse {
  name: string;
  projectId: string;
  files: FileHandle[];
  linters: LinterMapping;
  errorMessage?: string;
}

export interface LintResponse {
  status: string;
  linters: LinterMapping;
  lintFiles: {
    name: string;
    path: string;
    linter: string;
    lints: Lint[];
  }[];
  errorMessage?: string;
}

export interface SearchPatternsResponse {
  patterns: SearchPattern[];
  errorMessage?: string;
}

export interface GenericStatusResponse {
  success: boolean; //do I really need a success field? I can just check for the existence of the errorMessage field
  errorMessage?: string;
}
