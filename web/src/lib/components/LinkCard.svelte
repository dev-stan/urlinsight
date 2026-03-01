<script lang="ts">
	import { getLinkAnalytics } from '$lib/api';
	import type { Link, LinkAnalytics } from '$lib/types';
	import { ChevronDown, MousePointerClick, Users, ExternalLink } from 'lucide-svelte';
	import { slide } from 'svelte/transition';

	let { link }: { link: Link } = $props();

	let expanded = $state(false);
	let analytics: LinkAnalytics | null = $state(null);
	let loading = $state(false);

	async function toggleExpand() {
		expanded = !expanded;
		if (expanded && !analytics) {
			loading = true;
			try {
				analytics = await getLinkAnalytics(link.short_code);
			} catch {
				// silently fail — analytics section stays empty
			} finally {
				loading = false;
			}
		}
	}

	function getShortUrl(code: string): string {
		return `${window.location.origin}/api/redirect/${code}`;
	}
</script>

<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 transition-colors hover:border-zinc-700">
	<button onclick={toggleExpand} class="w-full cursor-pointer px-5 py-4 text-left">
		<div class="flex items-center justify-between gap-4">
			<div class="min-w-0 flex-1">
				<div class="flex items-center gap-2">
					<span class="font-medium text-zinc-50">/r/{link.short_code}</span>
					<a
						href={getShortUrl(link.short_code)}
						target="_blank"
						rel="noopener noreferrer"
						onclick={(e) => e.stopPropagation()}
						class="text-zinc-500 transition-colors hover:text-zinc-300"
					>
						<ExternalLink class="h-3.5 w-3.5" />
					</a>
				</div>
				<p class="mt-1 truncate text-sm text-zinc-500">{link.target_url}</p>
			</div>
			<ChevronDown
				class="h-5 w-5 shrink-0 text-zinc-500 transition-transform duration-200 {expanded
					? 'rotate-180'
					: ''}"
			/>
		</div>
	</button>

	{#if expanded}
		<div class="border-t border-zinc-800 px-5 py-4" transition:slide={{ duration: 200 }}>
			{#if loading}
				<div class="flex items-center gap-2 text-sm text-zinc-500">
					<div class="h-4 w-4 animate-spin rounded-full border-2 border-zinc-700 border-t-zinc-400"></div>
					Loading analytics...
				</div>
			{:else if analytics}
				<div class="mb-4 grid grid-cols-2 gap-3">
					<div class="rounded-lg bg-zinc-800/50 p-4">
						<div class="flex items-center gap-2 text-zinc-500">
							<MousePointerClick class="h-4 w-4" />
							<span class="text-xs font-medium uppercase tracking-wide">Clicks</span>
						</div>
						<p class="mt-1 text-2xl font-semibold text-zinc-50">
							{analytics.totals.clicks}
						</p>
					</div>
					<div class="rounded-lg bg-zinc-800/50 p-4">
						<div class="flex items-center gap-2 text-zinc-500">
							<Users class="h-4 w-4" />
							<span class="text-xs font-medium uppercase tracking-wide">Unique</span>
						</div>
						<p class="mt-1 text-2xl font-semibold text-zinc-50">
							{analytics.totals.unique_visitors}
						</p>
					</div>
				</div>

				{#if analytics.daily.length > 0}
					<table class="w-full text-sm">
						<thead>
							<tr class="text-left text-zinc-500">
								<th class="pb-2 font-medium">Date</th>
								<th class="pb-2 text-right font-medium">Clicks</th>
								<th class="pb-2 text-right font-medium">Unique</th>
							</tr>
						</thead>
						<tbody>
							{#each analytics.daily as day}
								<tr class="border-t border-zinc-800/50">
									<td class="py-2 text-zinc-300">{day.date}</td>
									<td class="py-2 text-right text-zinc-300">{day.clicks}</td>
									<td class="py-2 text-right text-zinc-300">{day.unique_visitors}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				{:else}
					<p class="text-sm text-zinc-500">No click data yet</p>
				{/if}
			{/if}
		</div>
	{/if}
</div>
