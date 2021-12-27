import { SearchPattern } from "@/components/types/interfaces";

export interface ProjectResponse {
  name: string;
  projectId: string;
  projectUrl: URL;
  sourcesUrl: URL;
  lintUrl: URL;
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
}
