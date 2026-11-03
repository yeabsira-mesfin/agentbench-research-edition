const base = (
  import.meta.env.VITE_API_BASE_URL ??
  (import.meta.env.DEV ? "http://localhost:8000" : "")
).replace(/\/$/, "");
export async function request<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(`${base}${path}`, {
      ...init,
      signal: controller.signal,
      headers: {
        ...(typeof init.body === "string"
          ? { "Content-Type": "application/json" }
          : {}),
        ...init.headers,
      },
    });
    if (!response.ok)
      throw new Error(
        `Request failed (${response.status}). Check API availability and try again.`,
      );
    return (await response.json()) as T;
  } catch (error) {
    if (controller.signal.aborted)
      throw new Error("The API took too long to respond. Please retry.");
    throw error instanceof Error
      ? error
      : new Error("Unable to reach the API.");
  } finally {
    clearTimeout(timer);
  }
}

