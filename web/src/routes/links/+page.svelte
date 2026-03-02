<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getLinks } from '$lib/api';
	import { getAuth } from '$lib/auth.svelte';
	import type { Link } from '$lib/types';
	import Header from '$lib/components/Header.svelte';
	import LinkCard from '$lib/components/LinkCard.svelte';
	import Mascot from '$lib/components/Mascot.svelte';
	import { fade } from 'svelte/transition';

	const auth = getAuth();

	let links: Link[] = $state([]);
	let loading = $state(true);

	onMount(async () => {
		await auth.init();
		if (!auth.isAuthenticated) {
			goto('/login');
			return;
		}
		try {
			links = await getLinks();
		} catch {
			// API unavailable
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>My Links - URLinsight</title>
</svelte:head>

<Header />

<main class="pt-24">
	<div class="mx-auto max-w-2xl px-4 sm:px-6">
		<h1 class="mb-6 text-xl font-semibold text-zinc-50 sm:text-2xl">My Links</h1>

		{#if loading}
			<div class="flex items-center gap-2 text-sm text-zinc-500">
				<div class="h-4 w-4 animate-spin rounded-full border-2 border-zinc-700 border-t-zinc-400"></div>
				Loading links...
			</div>
		{:else if links.length === 0}
			<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-10 text-center">
				<div class="flex justify-center">
					<Mascot size={64} animate />
				</div>
				<p class="mt-4 text-zinc-400">No links yet.</p>
				<a
					href="/"
					class="mt-3 inline-block rounded-lg bg-zinc-800 px-4 py-2 text-sm text-zinc-300 transition-colors hover:bg-zinc-700 hover:text-zinc-50"
				>
					Shorten your first link
				</a>
			</div>
		{:else}
			<div class="space-y-3">
				{#each links as link (link.short_code)}
					<div transition:fade={{ duration: 150 }}>
						<LinkCard {link} />
					</div>
				{/each}
			</div>
		{/if}
	</div>
</main>
