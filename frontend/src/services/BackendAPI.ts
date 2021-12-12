const apiAddress = "https://localhost:5000/api/";

export async function submitProject(): Promise<string> {
  const resp = await fetch(apiAddress + "projects");
  if (!resp.ok) {
    return null as any;
  }
  return await resp.json();
}

export async function getLint(): Promise<string> {
  return null as any;
}
