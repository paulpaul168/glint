import { FileHandle, Lint } from "@/components/types/interfaces";
import { SubmitProject } from "./types/api_requests_interfaces";
import {
  ProjectResponse,
  LintResponse,
  SearchPatternsResponse,
  ProjectDataResponse,
  ProjectListResponse,
  GenericStatusResponse,
} from "./types/api_responses_interfaces";

export const apiAddress = "http://localhost:5000/api/"; //don't like having to export that, but I think I need it to allow setting sensible default URLs. Do I even want that?

export async function getProjects(): Promise<ProjectListResponse> {
  const emptyResponse: ProjectListResponse = {
    projects: [],
    errorMessage: undefined,
  };

  let resp;
  try {
    resp = await fetch(apiAddress + "projects", {
      method: "GET",
    });
  } catch (error) {
    emptyResponse.errorMessage =
      "Fatal error while fetching projects: " + error;
    return emptyResponse;
  }

  if (!resp.ok) {
    emptyResponse.errorMessage =
      "Received non-OK response when fetching projects: " + resp.status;
    return emptyResponse;
  }
  const respJson = await resp.json();

  return respJson;
}

export async function getProjectData(id: string): Promise<ProjectDataResponse> {
  const emptyResponse: ProjectDataResponse = {
    name: "",
    projectId: "",
    files: [],
    linters: {},
  };

  let resp;
  try {
    resp = await fetch(apiAddress + "projects/" + id, {
      method: "GET",
    });
  } catch (error) {
    emptyResponse.errorMessage =
      "Fatal error while fetching project data: " + error;
    return emptyResponse;
  }

  if (!resp.ok) {
    emptyResponse.errorMessage =
      "Received non-OK response when fetching project data: " + resp.status;
    return emptyResponse;
  }
  const respJson = await resp.json();

  return respJson;
}

export async function submitProject(
  project: SubmitProject
): Promise<ProjectResponse> {
  const emptyProjectResp: ProjectResponse = {
    name: "",
    projectId: "",
    projectUrl: new URL(apiAddress),
    sourcesUrl: new URL(apiAddress),
    lintUrl: new URL(apiAddress),
  };

  let resp;
  try {
    resp = await fetch(apiAddress + "projects", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(project),
    });
  } catch (error) {
    emptyProjectResp.errorMessage =
      "Fatal error during fetch when submitting project: " + error;
    return emptyProjectResp;
  }

  if (!resp.ok) {
    emptyProjectResp.errorMessage =
      "non-OK message received while submitting project";
    return emptyProjectResp;
  }
  return await resp.json();
}

export async function deleteProject(
  id: string
): Promise<GenericStatusResponse> {
  const returnResponse: GenericStatusResponse = {
    success: false,
  };

  let resp;
  try {
    resp = await fetch(apiAddress + "projects/" + id, {
      method: "DELETE",
    });
  } catch (error) {
    returnResponse.success = false;
    returnResponse.errorMessage =
      "Fatal error during when deleting project: " + error;
    return returnResponse;
  }

  if (!resp.ok) {
    returnResponse.success = false;
    returnResponse.errorMessage =
      "Received non-OK response when fetching lint: " + resp.status;
    return returnResponse;
  }
  returnResponse.success = true;
  return returnResponse;
}

export async function overwriteFile(
  projectId: string,
  file: FileHandle
): Promise<GenericStatusResponse> {
  let resp;
  try {
    resp = await fetch(
      `${apiAddress}projects/${projectId}/sources/${file.name}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: FileList.name,
          path: file.path,
          content: file.content,
        }),
      }
    );
  } catch (error) {
    return {
      success: false,
      errorMessage:
        "Fatal error during saving file content (overwrite) " + error,
    };
  }

  if (!resp.ok) {
    return {
      success: false,
      errorMessage:
        "non-OK status received while overwriting file: " + resp.status,
    };
  }

  return { success: true };
}

export async function getLint(projectId: string): Promise<LintResponse> {
  let resp;
  const returnLint: LintResponse = {
    status: "",
    linters: {},
    lintFiles: [],
  };

  try {
    resp = await fetch(apiAddress + "projects/" + projectId + "/lint", {
      method: "GET",
    });
  } catch (error) {
    returnLint.status = "error";
    returnLint.errorMessage =
      "Fatal error while requesting Lint result: " + error;
    return returnLint;
  }

  if (!resp.ok) {
    returnLint.status = "error";
    returnLint.errorMessage =
      "Received non-OK response when fetching lint: " + resp.status;
    return returnLint;
  }
  const respJson = await resp.json();

  const lintFilesBuffer: {
    name: string;
    path: string;
    linter: string;
    lints: Lint[];
  }[] = [];
  if (respJson["status"] == "done") {
    respJson["files"].forEach(
      (
        file: {
          name: string;
          path: string;
          linter: string;
          lints: Lint[];
        },
        index: number
      ) => {
        lintFilesBuffer.push({
          name: file.name,
          path: file.path,
          linter: file.linter,
          lints: [],
        });

        for (const lint of file.lints) {
          const lintFile: Lint = lint;
          lintFile.fileName = file.name;
          lintFilesBuffer[index].lints.push(lintFile);
        }
      }
    );
  } else if (respJson["status"] != "processing") {
    //if linting is not done or still processing, an error occurred. right now we don't do anything special here, but we might get a "message" field or need to handle the status field differently in the future to get decent error messages
  }

  returnLint.status = respJson["status"];
  returnLint.linters = respJson["linters"];
  returnLint.lintFiles = lintFilesBuffer;
  return returnLint;
}

export async function getSearchPatterns(): Promise<SearchPatternsResponse> {
  let resp;
  let returnPatterns: SearchPatternsResponse = {
    patterns: [],
  };
  try {
    resp = await fetch(apiAddress + "searchPatterns", {
      method: "GET",
    });
  } catch (error) {
    returnPatterns.errorMessage =
      "Fatal error while requesting secrets search patterns: " + error;
    return returnPatterns;
  }

  if (!resp.ok) {
    returnPatterns.errorMessage =
      "Received non-OK response when fetching search patterns: " + resp.status;
    return returnPatterns;
  }

  try {
    returnPatterns = await resp.json();
  } catch (error) {
    returnPatterns.errorMessage =
      "Fatal error while parsing JSON from search patterns response: " + error;
  }

  return returnPatterns;
}
