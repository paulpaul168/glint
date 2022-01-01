import { FileHandle, Lint } from "@/components/types/interfaces";
import { SubmitProject } from "./types/api_requests_interfaces";
import {
  ProjectResponse,
  LintResponse,
  SearchPatternsResponse,
  ProjectDataResponse,
  ProjectListResponse,
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
    console.log("Fatal error while fetching projects", error);
    emptyResponse.errorMessage =
      "Fatal error while fetching projects: " + error;
    return emptyResponse;
  }

  if (!resp.ok) {
    console.log(
      "Received non-OK response when fetching projects: ",
      resp.status
    );
    emptyResponse.errorMessage =
      "Received non-OK response when fetching projects: " + resp.status;
    return emptyResponse;
  }
  const respJson = await resp.json();
  console.log("response:", respJson);

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
    console.log("Fatal error during fetch when submitting project:", error);
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

export async function overwriteFile(
  projectId: string,
  file: FileHandle
): Promise<{ success: boolean; errorMessage?: string }> {
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
    console.log("Fatal error during saving file content (overwrite):", error);
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
    linter: "unknown",
    lintFiles: [],
  };

  try {
    resp = await fetch(apiAddress + "projects/" + projectId + "/lint", {
      method: "GET",
    });
  } catch (error) {
    console.log("Fatal error during fetch when asking for lint", error);
    returnLint.status = "error";
    returnLint.errorMessage =
      "Fatal error while requesting Lint result: " + error;
    return returnLint;
  }

  if (!resp.ok) {
    console.log("Received non-OK response when fetching lint: ", resp.status);
    returnLint.status = "error";
    returnLint.errorMessage =
      "Received non-OK response when fetching lint: " + resp.status;
    return returnLint;
  }
  const respJson = await resp.json();

  const lintFilesBuffer: { name: string; path: string; lints: Lint[] }[] = [];
  if (respJson["status"] == "done") {
    respJson["files"].forEach(
      (
        file: {
          name: string;
          path: string;
          lints: Lint[];
        },
        index: number
      ) => {
        lintFilesBuffer.push({
          name: file.name,
          path: file.path,
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
  returnLint.linter = respJson["linter"];
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
    console.log("Fatal error during fetch when asking for patterns", error);
    returnPatterns.errorMessage =
      "Fatal error while requesting secrets search patterns: " + error;
    return returnPatterns;
  }

  if (!resp.ok) {
    console.log(
      "Received non-OK response when fetching search patterns: ",
      resp.status
    );
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
