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
  linter: string;
  lintFiles: {
    name: string;
    path: string;
    lints: Lint[];
  }[];
  errorMessage?: string;
}

export interface SearchPatternsResponse {
  patterns: SearchPattern[];
  errorMessage?: string;
}
