export async function getGod() {
    const resp = await fetch("http://localhost:5000/");
    if (!resp.ok)
    {
        return null;
    }
    return resp;
}