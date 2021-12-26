import { FileHandle, Lint } from "@/components/types/interfaces";
import { SubmitProject } from "./types/api_requests_interfaces";
import {
  ProjectResponse,
  LintResponse,
} from "./types/api_responses_interfaces";

export const apiAddress = "http://localhost:5000/api/"; //don't like having to export that, but I think I need it to allow setting sensible default URLs. Do I even want that?

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
    console.log(
      "Fatal error during fetch when submitting project:",
      error,
      "Aborting."
    );
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
    console.log("Fatal error during saving file content (overwrite), aborting");
    return {
      success: false,
      errorMessage:
        "Fatal error during saving file content (overwrite), aborting",
    };
  }

  if (!resp.ok) {
    return {
      success: false,
      errorMessage: "non-OK status received while overwriting file",
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
  } catch {
    console.log("Fatal error during fetch when asking for lint, aborting");
    returnLint.status = "error";
    returnLint.errorMessage =
      "Fatal error while requesting Lint result; fetch() threw Exception";
    return returnLint;
  }

  if (!resp.ok) {
    if (resp.status == 404) {
      //filter 404 out individually to circumvent that the backend doesn't properly work on this part yet.
      console.log("404 trying to get lint");
      /*return {
        status: "processing",
        linter: "unknown",
        lintFiles: [
          {
            name: "",
            path: "",
            lints: [],
          },
        ],
      };*/
    }
    console.log("Received non-OK response when fetching lint");
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
