export const supportedLanguages = ["python", "javascript", "html", "markdown"]; //I dislike this approach, but I can't think of anything better at this point in time

export function getLanguage(extension: string): string {
  let language = "";
  switch (extension) {
    case "py":
      language = "python";
      break;
    case "ts":
    case "js":
      language = "javascript";
      break;
    case "vue":
      language = "html";
      break;
    case "md":
      language = "markdown";
      break;
    default:
      console.log("Couldn't detect language");
      return "txt";
  }
  return language;
}
