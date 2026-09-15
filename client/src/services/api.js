const API_BASE = 'http://localhost:8000';

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function request(url, options = {}) {
  const response = await fetch(`${API_BASE}${url}`, options);
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new ApiError(data.error || 'Request failed', response.status);
  }
  return response;
}

export async function uploadVideo(file) {
  const formData = new FormData();
  formData.append('file', file);
  const response = await request('/api/v1/upload', {
    method: 'POST',
    body: formData,
  });
  return response.json();
}

export async function getConversionStatus(id) {
  const response = await request(`/api/v1/conversion/${id}/status`);
  return response.json();
}

export async function getConversionFrames(id) {
  const response = await request(`/api/v1/conversion/${id}/frames`);
  return response.json();
}

export function getAudioUrl(id) {
  return `${API_BASE}/api/v1/conversion/${id}/audio`;
}

export async function deleteConversion(id) {
  try {
    await request(`/api/v1/conversion/${id}`, { method: 'DELETE' });
  } catch {
    // Ignore errors on cleanup
  }
}

let currentConversionId = null;

export function setCurrentConversion(id) {
  currentConversionId = id;
}

export function setupCleanupOnUnload() {
  window.addEventListener('beforeunload', () => {
    if (currentConversionId) {
      navigator.sendBeacon(`${API_BASE}/api/v1/conversion/${currentConversionId}`);
    }
  });
}

export { ApiError };
