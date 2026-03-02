<script lang="ts">
	import { goto } from '$app/navigation';
	import { register as apiRegister, login as apiLogin } from '$lib/api';
	import { getAuth } from '$lib/auth.svelte';
	import Mascot from '$lib/components/Mascot.svelte';

	const auth = getAuth();

	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		error = '';

		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}

		if (password.length < 6) {
			error = 'Password must be at least 6 characters';
			return;
		}

		loading = true;
		try {
			await apiRegister(email, password);
			const res = await apiLogin(email, password);
			await auth.loginUser(res.access_token);
			goto('/');
		} catch (err) {
			error = err instanceof Error ? err.message : 'Registration failed';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Register - URLinsight</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center px-4 sm:px-6">
	<div class="w-full max-w-sm">
		<div class="mb-8 flex justify-center">
			<Mascot size={80} animate />
		</div>

		<h1 class="mb-2 text-center text-2xl font-semibold text-zinc-50">Create an account</h1>
		<p class="mb-8 text-center text-sm text-zinc-500">Save your shortened links and track analytics</p>

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
					placeholder="At least 6 characters"
				/>
			</div>

			<div>
				<label for="confirm" class="mb-1.5 block text-xs font-medium tracking-wide text-zinc-400 uppercase">Confirm password</label>
				<input
					id="confirm"
					type="password"
					bind:value={confirmPassword}
					required
					class="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3 text-sm text-zinc-50 outline-none transition-colors placeholder:text-zinc-600 focus:border-zinc-600"
					placeholder="Repeat your password"
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
				{loading ? 'Creating account...' : 'Create account'}
			</button>
		</form>

		<p class="mt-6 text-center text-sm text-zinc-500">
			Already have an account?
			<a href="/login" class="text-zinc-300 hover:text-zinc-50">Sign in</a>
		</p>
	</div>
</div>
