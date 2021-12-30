export const supportedLanguages = [
  "python",
  "javascript",
  "html",
  "markdown",
  "plain",
]; //I dislike this approach, but I can't think of anything better at this point in time

export function getLanguage(fileName: string | undefined): string {
  if (fileName == undefined) {
    return "txt";
  }
  const extension = fileName.split(".").pop();
  if (extension == undefined) {
    return "txt";
  }
  let language = "";
  switch (extension) {
    case "py":
      language = "python";
      break;
    case "ts":
      language = "typescript";
      break;
    case "js":
      language = "javascript";
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
      console.log("Couldn't detect language");
      return "txt";
  }
  return language;
}
