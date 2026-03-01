<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { changePassword } from '$lib/api';
	import { getAuth } from '$lib/auth.svelte';
	import Header from '$lib/components/Header.svelte';
	import Mascot from '$lib/components/Mascot.svelte';
	import { LogOut, KeyRound, Check, AlertCircle } from 'lucide-svelte';
	import { fade } from 'svelte/transition';

	const auth = getAuth();

	let currentPassword = $state('');
	let newPassword = $state('');
	let confirmPassword = $state('');
	let passwordLoading = $state(false);
	let passwordError = $state('');
	let passwordSuccess = $state(false);

	onMount(async () => {
		await auth.init();
		if (!auth.isAuthenticated) {
			goto('/login');
		}
	});

	function handleLogout() {
		auth.logout();
		goto('/');
	}

	async function handlePasswordChange(e: SubmitEvent) {
		e.preventDefault();
		passwordError = '';
		passwordSuccess = false;

		if (newPassword !== confirmPassword) {
			passwordError = 'New passwords do not match';
			return;
		}
		if (newPassword.length < 6) {
			passwordError = 'New password must be at least 6 characters';
			return;
		}

		passwordLoading = true;
		try {
			await changePassword(currentPassword, newPassword);
			passwordSuccess = true;
			currentPassword = '';
			newPassword = '';
			confirmPassword = '';
			setTimeout(() => (passwordSuccess = false), 3000);
		} catch (err) {
			passwordError = err instanceof Error ? err.message : 'Failed to change password';
		} finally {
			passwordLoading = false;
		}
	}
</script>

<svelte:head>
	<title>Profile - URLinsight</title>
</svelte:head>

<Header />

<main class="pt-24">
	<div class="mx-auto max-w-xl px-6">
		{#if auth.loading}
			<div class="flex items-center justify-center py-20">
				<div class="h-6 w-6 animate-spin rounded-full border-2 border-zinc-700 border-t-zinc-400"></div>
			</div>
		{:else if auth.user}
			<!-- Account header -->
			<div class="mb-8 flex items-center gap-5">
				<Mascot size={56} />
				<div>
					<h1 class="text-xl font-semibold text-zinc-50">Account</h1>
					<p class="text-sm text-zinc-500">{auth.user.email}</p>
				</div>
			</div>

			<!-- Change password -->
			<section class="mb-8 rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
				<div class="mb-5 flex items-center gap-2 text-zinc-300">
					<KeyRound class="h-4 w-4" />
					<h2 class="text-sm font-semibold uppercase tracking-wide">Change password</h2>
				</div>

				<form onsubmit={handlePasswordChange} class="space-y-4">
					<div>
						<label for="current" class="mb-1 block text-xs text-zinc-500">Current password</label>
						<input
							id="current"
							type="password"
							bind:value={currentPassword}
							required
							class="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-2.5 text-sm text-zinc-50 outline-none transition-colors placeholder:text-zinc-600 focus:border-zinc-600"
						/>
					</div>
					<div>
						<label for="new" class="mb-1 block text-xs text-zinc-500">New password</label>
						<input
							id="new"
							type="password"
							bind:value={newPassword}
							required
							minlength="6"
							class="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-2.5 text-sm text-zinc-50 outline-none transition-colors placeholder:text-zinc-600 focus:border-zinc-600"
						/>
					</div>
					<div>
						<label for="confirm" class="mb-1 block text-xs text-zinc-500">Confirm new password</label>
						<input
							id="confirm"
							type="password"
							bind:value={confirmPassword}
							required
							minlength="6"
							class="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-2.5 text-sm text-zinc-50 outline-none transition-colors placeholder:text-zinc-600 focus:border-zinc-600"
						/>
					</div>

					{#if passwordError}
						<div class="flex items-center gap-2 text-sm text-red-400" transition:fade={{ duration: 150 }}>
							<AlertCircle class="h-4 w-4 shrink-0" />
							{passwordError}
						</div>
					{/if}

					{#if passwordSuccess}
						<div class="flex items-center gap-2 text-sm text-emerald-400" transition:fade={{ duration: 150 }}>
							<Check class="h-4 w-4 shrink-0" />
							Password updated
						</div>
					{/if}

					<button
						type="submit"
						disabled={passwordLoading}
						class="rounded-lg bg-zinc-50 px-4 py-2 text-sm font-medium text-zinc-950 transition-colors hover:bg-white disabled:opacity-50"
					>
						{passwordLoading ? 'Updating...' : 'Update password'}
					</button>
				</form>
			</section>

			<!-- Sign out -->
			<section class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
				<div class="flex items-center justify-between">
					<div>
						<h2 class="text-sm font-semibold text-zinc-300">Sign out</h2>
						<p class="mt-1 text-xs text-zinc-500">End your current session</p>
					</div>
					<button
						onclick={handleLogout}
						class="flex items-center gap-2 rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-400 transition-colors hover:border-zinc-600 hover:text-zinc-50"
					>
						<LogOut class="h-4 w-4" />
						Sign out
					</button>
				</div>
			</section>
		{/if}
	</div>
</main>
