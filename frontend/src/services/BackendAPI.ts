import { FileHandle, Lint } from "@/components/types/interfaces";
import {
  EditProject,
  SearchPatternRequest,
  SubmitProject,
} from "./types/api_requests_interfaces";
import {
  ProjectResponse,
  LintResponse,
  SearchPatternsResponse,
  ProjectDataResponse,
  ProjectListResponse,
  GenericStatusResponse,
  AddFileResponse,
  LinterListResponse,
  AddSearchPatternResponse,
} from "./types/api_responses_interfaces";

export const apiAddress =
  location.protocol + "//" + location.hostname + ":5000/api/"; //don't like having to export that, but I think I need it to allow setting sensible default URLs. Do I even want that?

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

  if (id == "") {
    emptyResponse.errorMessage = "Tried loading project data with empty ID";
    return emptyResponse;
  }

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
  for (const file of respJson.files) {
    console.log("resp", file.path);
  }

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

export async function editProject(
  id: string,
  data: EditProject
): Promise<GenericStatusResponse> {
  const returnResponse: GenericStatusResponse = {
    success: false,
  };

  let resp;
  try {
    resp = await fetch(apiAddress + "projects/" + id, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  } catch (error) {
    returnResponse.success = false;
    returnResponse.errorMessage = "Fatal error while editing project: " + error;
    return returnResponse;
  }

  if (!resp.ok) {
    returnResponse.success = false;
    returnResponse.errorMessage =
      "Received non-OK response while editing project: " + resp.status;
    return returnResponse;
  }
  returnResponse.success = true;
  return returnResponse;
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
    returnResponse.errorMessage = "Fatal error when deleting project: " + error;
    return returnResponse;
  }

  if (!resp.ok) {
    returnResponse.success = false;
    returnResponse.errorMessage =
      "Received non-OK response when deleting project: " + resp.status;
    return returnResponse;
  }
  returnResponse.success = true;
  return returnResponse;
}

export async function overwriteFile(
  projectId: string,
  file: FileHandle,
  oldPath?: string
): Promise<GenericStatusResponse> {
  let resp;
  const path = oldPath == undefined ? file.path : oldPath;
  try {
    resp = await fetch(`${apiAddress}projects/${projectId}/sources/${path}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        path: file.path,
        content: file.content,
      }),
    });
  } catch (error) {
    return {
      success: false,
      errorMessage:
        oldPath == undefined
          ? "Fatal error during saving file content (overwrite) "
          : "Fatal error during file rename " + error,
    };
  }

  if (!resp.ok) {
    return {
      success: false,
      errorMessage:
        oldPath == undefined
          ? "Received non-OK response while overwriting file: "
          : "Received non-OK response while renaming file: " + resp.status,
    };
  }

  return { success: true };
}

export async function addFile(
  projectId: string,
  file: FileHandle
): Promise<AddFileResponse> {
  let resp;
  try {
    console.log("add file", file);
    resp = await fetch(`${apiAddress}projects/${projectId}/sources`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        filePath: file.path,
        content: file.content,
      }),
    });
  } catch (error) {
    return {
      filePath: "",
      fileUrl: new URL(apiAddress),
      errorMessage: "Fatal error when adding file to project: " + error,
    };
  }

  if (!resp.ok) {
    return {
      filePath: "",
      fileUrl: new URL(apiAddress),
      errorMessage:
        "Received non-OK response while saving file: " + resp.status,
    };
  }

  const respJson = await resp.json();
  const returnDict: AddFileResponse = {
    filePath: respJson["filePath"],
    fileUrl: new URL(
      apiAddress + decodeURI(respJson["fileUrl"]).replace("/api/", "")
    ), //do I need to do this? if so, don't I need to do this everywhere with URLs?
  };
  return returnDict;
}

export async function deleteFile(
  projectId: string,
  filePath: string
): Promise<GenericStatusResponse> {
  const returnResponse: GenericStatusResponse = {
    success: false,
  };

  let resp;
  try {
    resp = await fetch(
      `${apiAddress}projects/${projectId}/sources/${filePath}`,
      {
        method: "DELETE",
      }
    );
  } catch (error) {
    returnResponse.success = false;
    returnResponse.errorMessage = "Fatal error when deleting file: " + error;
    return returnResponse;
  }

  if (!resp.ok) {
    returnResponse.success = false;
    returnResponse.errorMessage =
      "Received non-OK response when deleting file: " + resp.status;
    return returnResponse;
  }
  returnResponse.success = true;
  return returnResponse;
}

export async function getLinters(): Promise<LinterListResponse> {
  const emptyResponse: LinterListResponse = {};

  let resp;
  try {
    resp = await fetch(apiAddress + "linters", {
      method: "GET",
    });
  } catch (error) {
    emptyResponse.errorMessage = "Fatal error while fetching linters: " + error;
    return emptyResponse;
  }

  if (!resp.ok) {
    emptyResponse.errorMessage =
      "Received non-OK response when fetching linters: " + resp.status;
    return emptyResponse;
  }

  return await resp.json();
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
  let returnPatterns: SearchPatternsResponse = {};
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
    if (resp.status == 404) {
      return returnPatterns;
    }
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

export async function setSearchPattern(
  pattern: SearchPatternRequest,
  patternId?: string
): Promise<AddSearchPatternResponse> {
  let resp;
  const method = patternId == undefined ? "POST" : "PUT";
  const addressEnd = patternId == undefined ? "" : `/${patternId}`;
  try {
    resp = await fetch(`${apiAddress}searchPatterns${addressEnd}`, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(pattern),
    });
  } catch (error) {
    return {
      patternName: "",
      patternId: "",
      regex: "",
      errorMessage: "Fatal error while setting search pattern: " + error,
    };
  }

  if (!resp.ok) {
    return {
      patternName: "",
      patternId: "",
      regex: "",
      errorMessage:
        "Received non-OK response while setting search pattern: " + resp.status,
    };
  }

  return await resp.json();
}

export async function deleteSearchPattern(
  patternId: string
): Promise<GenericStatusResponse> {
  let resp;
  try {
    resp = await fetch(`${apiAddress}searchPatterns/${patternId}`, {
      method: "DELETE",
    });
  } catch (error) {
    return {
      success: false,
      errorMessage: "Fatal error while deleting search pattern: " + error,
    };
  }

  if (!resp.ok) {
    return {
      success: false,
      errorMessage:
        "Received non-OK response while deleting search pattern: " +
        resp.status,
    };
  }

  const respJson = await resp.json();
  if (respJson.status != "OK") {
    return { success: false, errorMessage: "Unknown Error" };
  }
  return { success: true };
}
