export async function submitProject(): Promise<string> {
  const resp = await fetch("");
  if (!resp.ok) {
    return null as any;
  }
  return await resp.json();
}
