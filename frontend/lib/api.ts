const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function fetchCompanies(params?: Record<string, string>) {
  const url = new URL(`${API_BASE_URL}/companies`);
  if (params) {
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key] || ''));
  }
  const res = await fetch(url.toString(), { cache: 'no-store' });
  if (!res.ok) return [];
  return res.json();
}

export async function fetchInvestors() {
  const res = await fetch(`${API_BASE_URL}/investors`, { cache: 'no-store' });
  if (!res.ok) return [];
  return res.json();
}
