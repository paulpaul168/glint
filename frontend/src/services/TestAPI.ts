export async function getGod(): Promise<string> {
  const resp = await fetch("http://localhost:5000/");
  if (!resp.ok) {
    return null as any;
  }
  const god = (await resp.json())["god"];
  console.log("awaited god", god);
  return god;
}
