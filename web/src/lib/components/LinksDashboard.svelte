<script lang="ts">
	import type { Link } from '$lib/types';
	import LinkCard from './LinkCard.svelte';
	import { fade } from 'svelte/transition';

	let { links, loading }: { links: Link[]; loading: boolean } = $props();
</script>

<section class="mx-auto max-w-2xl px-6">
	<h2 class="mb-6 text-xl font-semibold text-zinc-50">Your Links</h2>

	{#if loading}
		<div class="flex items-center gap-2 text-sm text-zinc-500">
			<div class="h-4 w-4 animate-spin rounded-full border-2 border-zinc-700 border-t-zinc-400"></div>
			Loading links...
		</div>
	{:else if links.length === 0}
		<p class="text-zinc-500">No links yet. Create your first one above.</p>
	{:else}
		<div class="space-y-3">
			{#each links as link (link.short_code)}
				<div transition:fade={{ duration: 150 }}>
					<LinkCard {link} />
				</div>
			{/each}
		</div>
	{/if}
</section>
