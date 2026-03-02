<script lang="ts">
	import { goto } from '$app/navigation';
	import { login as apiLogin } from '$lib/api';
	import { getAuth } from '$lib/auth.svelte';
	import Mascot from '$lib/components/Mascot.svelte';

	const auth = getAuth();

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		error = '';
		loading = true;
		try {
			const res = await apiLogin(email, password);
			await auth.loginUser(res.access_token);
			goto('/');
		} catch (err) {
			error = err instanceof Error ? err.message : 'Login failed';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Login - URLinsight</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center px-4 sm:px-6">
	<div class="w-full max-w-sm">
		<div class="mb-8 flex justify-center">
			<Mascot size={80} />
		</div>

		<h1 class="mb-2 text-center text-2xl font-semibold text-zinc-50">Welcome back</h1>
		<p class="mb-8 text-center text-sm text-zinc-500">Sign in to see your links and analytics</p>

		<form onsubmit={handleSubmit} class="space-y-4">
			<div>
				<label for="email" class="mb-1.5 block text-xs font-medium tracking-wide text-zinc-400 uppercase">Email</label>
				<input
					id="email"
					type="email"
					bind:value={email}
					required
					class="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3 text-sm text-zinc-50 outline-none transition-colors placeholder:text-zinc-600 focus:border-zinc-600"
					placeholder="you@example.com"
				/>
			</div>

			<div>
				<label for="password" class="mb-1.5 block text-xs font-medium tracking-wide text-zinc-400 uppercase">Password</label>
				<input
					id="password"
					type="password"
					bind:value={password}
					required
					class="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3 text-sm text-zinc-50 outline-none transition-colors placeholder:text-zinc-600 focus:border-zinc-600"
					placeholder="Your password"
				/>
			</div>

			{#if error}
				<p class="text-sm text-red-400">{error}</p>
			{/if}

			<button
				type="submit"
				disabled={loading}
				class="w-full rounded-lg bg-zinc-50 py-3 text-sm font-medium text-zinc-950 transition-colors hover:bg-white disabled:opacity-50"
			>
				{loading ? 'Signing in...' : 'Sign in'}
			</button>
		</form>

		<p class="mt-6 text-center text-sm text-zinc-500">
			Don't have an account?
			<a href="/register" class="text-zinc-300 hover:text-zinc-50">Create one</a>
		</p>
	</div>
</div>
