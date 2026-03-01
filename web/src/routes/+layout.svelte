<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>URLinsight</title>
</svelte:head>

<div class="flex min-h-screen flex-col">
	<div class="flex-1">
		{@render children()}
	</div>
	<footer class="border-t border-zinc-800/50 py-6 text-center text-sm text-zinc-600">
		URLinsight is an open source project on <a href="https://github.com/dev-stan/urlinsight" class="text-zinc-500 underline decoration-zinc-700 underline-offset-2 hover:text-zinc-400">GitHub</a>.
	</footer>
</div>
