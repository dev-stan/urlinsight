<script lang="ts">
	import Mascot from './Mascot.svelte';
	import { X } from 'lucide-svelte';
	import { slide } from 'svelte/transition';

	let visible = $state(true);

	function dismiss() {
		visible = false;
		if (typeof sessionStorage !== 'undefined') {
			sessionStorage.setItem('guest_banner_dismissed', '1');
		}
	}

	if (typeof sessionStorage !== 'undefined' && sessionStorage.getItem('guest_banner_dismissed')) {
		visible = false;
	}
</script>

{#if visible}
	<div
		class="relative overflow-hidden border-b border-amber-900/30 bg-gradient-to-r from-amber-950/40 via-zinc-900 to-amber-950/40"
		transition:slide={{ duration: 300 }}
	>
		<div class="mx-auto flex max-w-3xl items-start gap-3 px-4 py-3 sm:items-center sm:gap-4 sm:px-6">
			<div class="hidden shrink-0 sm:block">
				<Mascot size={40} animate />
			</div>
			<p class="flex-1 text-sm text-zinc-300">
				<span class="font-medium text-amber-200">Hey there!</span>
				Your shortened links won't be saved.
				<a href="/register" class="font-medium text-zinc-50 underline decoration-zinc-500 underline-offset-2 hover:decoration-zinc-300">Create an account</a>
				to keep your links and track analytics.
			</p>
			<button
				onclick={dismiss}
				class="shrink-0 rounded p-1 text-zinc-500 transition-colors hover:text-zinc-300"
				aria-label="Dismiss"
			>
				<X class="h-4 w-4" />
			</button>
		</div>
	</div>
{/if}
