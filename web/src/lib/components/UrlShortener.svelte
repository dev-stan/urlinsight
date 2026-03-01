<script lang="ts">
	import { createLink } from '$lib/api';
	import type { Link } from '$lib/types';
	import { Copy, Check, ArrowRight, Loader2 } from 'lucide-svelte';
	import { fade } from 'svelte/transition';

	let { onLinkCreated }: { onLinkCreated: (link: Link) => void } = $props();

	let url = $state('');
	let result: Link | null = $state(null);
	let loading = $state(false);
	let error = $state('');
	let copied = $state(false);

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		if (!url.trim()) return;

		loading = true;
		error = '';
		result = null;

		try {
			result = await createLink(url.trim());
			onLinkCreated(result);
			url = '';
		} catch {
			error = 'Failed to shorten URL. Please try again.';
		} finally {
			loading = false;
		}
	}

	function getShortUrl(shortCode: string): string {
		return `${window.location.origin}/api/redirect/${shortCode}`;
	}

	async function copyToClipboard() {
		if (!result) return;
		try {
			await navigator.clipboard.writeText(getShortUrl(result.short_code));
			copied = true;
			setTimeout(() => (copied = false), 2000);
		} catch {
			copied = false;
		}
	}
</script>

<section class="mx-auto max-w-2xl px-6 text-center">
	<h1 class="mb-3 text-4xl font-semibold tracking-tight text-zinc-50">Shorten your links</h1>
	<p class="mb-10 text-lg text-zinc-400">Create short, trackable links in seconds</p>

	<form onsubmit={handleSubmit}>
		<div
			class="flex items-center rounded-2xl border border-zinc-800 bg-zinc-900 pr-2 transition-colors focus-within:border-zinc-600"
		>
			<input
				type="url"
				bind:value={url}
				placeholder="Paste your long URL here..."
				required
				class="flex-1 bg-transparent px-5 py-4 text-zinc-50 outline-none placeholder:text-zinc-500"
			/>
			<button
				type="submit"
				disabled={loading}
				class="flex items-center gap-2 rounded-xl bg-zinc-50 px-5 py-2.5 font-medium text-zinc-950 transition-colors hover:bg-white disabled:opacity-50"
			>
				{#if loading}
					<Loader2 class="h-4 w-4 animate-spin" />
					Shortening
				{:else}
					<ArrowRight class="h-4 w-4" />
					Shorten
				{/if}
			</button>
		</div>
	</form>

	{#if error}
		<p class="mt-4 text-sm text-red-400" transition:fade={{ duration: 150 }}>{error}</p>
	{/if}

	{#if result}
		<div
			class="mt-6 rounded-xl border border-zinc-800 bg-zinc-900/50 p-5"
			transition:fade={{ duration: 200 }}
		>
			<div class="flex items-center justify-between gap-4">
				<div class="min-w-0 text-left">
					<p class="mb-1 text-xs font-medium tracking-wide text-zinc-500 uppercase">
						Shortened URL
					</p>
					<a
						href={getShortUrl(result.short_code)}
						target="_blank"
						rel="noopener noreferrer"
						class="text-lg font-medium text-zinc-50 hover:underline"
					>
						{window.location.host}/r/{result.short_code}
					</a>
					<p class="mt-1 truncate text-sm text-zinc-500">
						{result.target_url}
					</p>
				</div>
				<button
					onclick={copyToClipboard}
					class="flex shrink-0 items-center gap-1.5 rounded-lg border border-zinc-700 px-3 py-2 text-sm text-zinc-300 transition-colors hover:bg-zinc-800"
				>
					{#if copied}
						<Check class="h-4 w-4 text-emerald-400" />
						<span class="text-emerald-400">Copied</span>
					{:else}
						<Copy class="h-4 w-4" />
						Copy
					{/if}
				</button>
			</div>
		</div>
	{/if}
</section>
