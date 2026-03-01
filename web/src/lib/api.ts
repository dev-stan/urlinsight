import type { Link, LinkAnalytics, TokenResponse, User } from './types';

const BASE = '/api';

function authHeaders(): Record<string, string> {
	const token = typeof localStorage !== 'undefined' ? localStorage.getItem('token') : null;
	if (!token) return {};
	return { Authorization: `Bearer ${token}` };
}

// --- Links ---

export async function createLink(targetUrl: string): Promise<Link> {
	const res = await fetch(`${BASE}/links`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json', ...authHeaders() },
		body: JSON.stringify({ target_url: targetUrl })
	});
	if (!res.ok) throw new Error('Failed to create link');
	return res.json();
}

export async function getLinks(): Promise<Link[]> {
	const res = await fetch(`${BASE}/links`, { headers: authHeaders() });
	if (!res.ok) throw new Error('Failed to fetch links');
	return res.json();
}

export async function getLinkAnalytics(shortCode: string): Promise<LinkAnalytics> {
	const res = await fetch(`${BASE}/links/${shortCode}/analytics`);
	if (!res.ok) throw new Error('Failed to fetch analytics');
	return res.json();
}

// --- Auth ---

export async function register(email: string, password: string): Promise<User> {
	const res = await fetch(`${BASE}/auth/register`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ email, password })
	});
	if (res.status === 409) throw new Error('Email already registered');
	if (!res.ok) throw new Error('Registration failed');
	return res.json();
}

export async function login(email: string, password: string): Promise<TokenResponse> {
	const res = await fetch(`${BASE}/auth/login`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ email, password })
	});
	if (res.status === 401) throw new Error('Invalid email or password');
	if (!res.ok) throw new Error('Login failed');
	return res.json();
}

export async function getMe(): Promise<User> {
	const res = await fetch(`${BASE}/auth/me`, { headers: authHeaders() });
	if (!res.ok) throw new Error('Not authenticated');
	return res.json();
}

export async function changePassword(currentPassword: string, newPassword: string): Promise<void> {
	const res = await fetch(`${BASE}/auth/password`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json', ...authHeaders() },
		body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
	});
	if (res.status === 401) throw new Error('Current password is incorrect');
	if (!res.ok) throw new Error('Failed to change password');
}
