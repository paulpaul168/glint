import { FileHandle, LintEvent, Lint } from "@/components/types/interfaces";
import { Dictionary } from "vue-router/types/router";

const apiAddress = "https://localhost:5000/api/";

export async function submitProject(
  name = "DefaultProject",
  files: FileHandle[],
  language = "auto",
  linter = "auto"
): Promise<string> {
  //init request data structure
  const request = {
    name: name,
    files: [] as Dictionary<string>[], //there has to be a nicer way of doing this
    language: language,
    linter: linter,
  };

  //enter files to push in request data
  for (const file of files) {
    const transmitFile = {
      name: file.name,
      path: file.path,
      content: file.content,
    };
    request.files.push(transmitFile);
  }

  let resp;
  try {
    resp = await fetch(apiAddress + "projects", {
      method: "POST",
      body: JSON.stringify(request),
    });
  } catch {
    console.log("Fatal error during fetch when submitting project, aborting");
    return ""; //TODO this should probably return some error code that can be read and properly reacted to
  }

  if (!resp.ok) {
    return null as any;
  }
  return await resp.json();
}

export async function getLint(projectId: string): Promise<LintEvent> {
  let resp;
  try {
    resp = await fetch(apiAddress + "projects/" + projectId + "/lint/", {
      method: "GET",
    });
  } catch {
    console.log("Fatal error during fetch when asking for lint, aborting");
    return {
      status:
        "Fatal error while requesting Lint result; fetch() threw Exception",
      linter: "unknown",
      lintFiles: [
        {
          name: "",
          path: "",
          lints: [],
        },
      ],
    };
  }
  if (!resp.ok) {
    //TODO if we really change http header on errors this handling will need to be updated
    return null as any;
  }
  const respJson = await resp.json();

  const lintEvent: LintEvent = {
    status: respJson["status"],
    linter: respJson["linter"],
    lintFiles: [
      {
        //data format between internal lintevent interface and json api differs slightly, needs to be converted after the fact
        name: "",
        path: "",
        lints: [],
      },
    ],
  };

  if (lintEvent.status == "done") {
    respJson["files"].forEach(
      (
        file: {
          name: string;
          path: string;
          lints: Lint[];
        },
        index: number
      ) => {
        lintEvent.lintFiles.push({
          name: file.name,
          path: file.path,
          lints: [],
        });

        for (const lint of file.lints) {
          const lintFile: Lint = lint;
          lintFile.fileName = file.name;
          /*const lintFile: Lint = {
            fileName: file.name,
            line: lint.line,
            endLine: lint.endLine,
            column: lint.column,
            endColumn: lint.endColumn,
            header: lint.header,
            message: lint.message,
            url: lint.url,
          };*/
          lintEvent.lintFiles[index].lints.push(lintFile);
        }
      }
    );
  } else if (lintEvent.status != "processing") {
    //if linting is not done or still processing, an error occurred. right now we don't do anything special here, but we might get a "message" field or need to handle the status field differently in the future to get decent error messages
  }

  return lintEvent;
}
