export async function fetchOrbit(params) {
  const res = await fetch("/api/orbit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  return res.json();
}