<script lang="ts">
	import { onMount } from 'svelte';
	import { getAuth } from '$lib/auth.svelte';
	import type { Link } from '$lib/types';
	import Header from '$lib/components/Header.svelte';
	import UrlShortener from '$lib/components/UrlShortener.svelte';
	import GuestBanner from '$lib/components/GuestBanner.svelte';
	import Mascot from '$lib/components/Mascot.svelte';

	const auth = getAuth();

	onMount(() => auth.init());

	function handleLinkCreated(link: Link) {
		// Link created — if authenticated it's saved server-side,
		// the user can view it on /links
	}
</script>

<Header />

<main class="pt-16">
	{#if !auth.loading && !auth.isAuthenticated}
		<GuestBanner />
	{/if}

	<div class="flex min-h-[70vh] items-center justify-center py-20">
		<div class="text-center">
			<div class="mb-8 flex justify-center">
				<Mascot size={100} animate />
			</div>
			<UrlShortener onLinkCreated={handleLinkCreated} />
		</div>
	</div>
</main>
