import { FileHandle } from "@/components/types/interfaces";
import { Dictionary } from "vue-router/types/router";

const apiAddress = "https://localhost:5000/api/";

export async function submitProject(
  name = "DefaultProject",
  files: FileHandle[],
  language = "auto",
  linter = "auto"
): Promise<string> {
  const request = {
    name: name,
    files: [] as Dictionary<string>[], //there has to be a nicer way of doing this
    language: language,
    linter: linter,
  };

  for (const file of files) {
    const transmitFile = {
      name: file.name,
      path: file.path,
      content: file.content,
    };
    request.files.push(transmitFile);
  }

  const resp = await fetch(apiAddress + "projects", {
    method: "POST",
    body: JSON.stringify(request),
  });
  if (!resp.ok) {
    return null as any;
  }
  return await resp.json();
}

export async function getLint(): Promise<string> {
  return null as any;
}
