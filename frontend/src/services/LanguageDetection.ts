export const supportedLanguages = [
  "python",
  "javascript",
  "typescript",
  "php",
  "go",
  "c",
  "cpp",
  "rust",
  "html",
  "plain",
]; //I dislike this approach, but I can't think of anything better at this point in time

export function getLanguage(fileName: string | undefined): string {
  if (fileName == undefined) {
    return "txt";
  }
  const extension = fileName.split(".").pop();
  if (extension == undefined || extension == "" || extension == fileName) {
    //no extension specified or somehow extension is empty
    return "txt";
  }
  let language = "";
  switch (extension) {
    case "py":
      language = "python";
      break;
    case "js":
      language = "javascript";
      break;
    case "ts":
      language = "typescript";
      break;
    case "php":
      language = "php";
      break;
    case "go":
      language = "go";
      break;
    case "c":
    case "h":
      language = "c";
      break;
    case "cpp":
    case "hpp":
      language = "cpp";
      break;
    case "rs":
      language = "rust";
      break;
    case "vue":
      language = "html";
      break;
    case "md":
      language = "markdown";
      break;
    case "plain":
      return "txt";
    default:
      console.log("Couldn't detect language", fileName);
      return "txt";
  }
  return language;
}
