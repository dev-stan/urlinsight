import { getMe } from '$lib/api';
import type { User } from '$lib/types';

let user = $state<User | null>(null);
let loading = $state(true);
let initialized = $state(false);

export function getAuth() {
	async function init() {
		if (initialized) return;
		initialized = true;
		const token = typeof localStorage !== 'undefined' ? localStorage.getItem('token') : null;
		if (!token) {
			loading = false;
			return;
		}
		try {
			user = await getMe();
		} catch {
			localStorage.removeItem('token');
		} finally {
			loading = false;
		}
	}

	function setToken(token: string) {
		localStorage.setItem('token', token);
	}

	async function loginUser(token: string) {
		setToken(token);
		user = await getMe();
	}

	function logout() {
		localStorage.removeItem('token');
		user = null;
	}

	return {
		get user() {
			return user;
		},
		get loading() {
			return loading;
		},
		get isAuthenticated() {
			return user !== null;
		},
		init,
		loginUser,
		logout
	};
}
