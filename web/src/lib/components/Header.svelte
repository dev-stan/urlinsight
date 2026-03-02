<script lang="ts">
	import { getAuth } from '$lib/auth.svelte';
	import { afterNavigate } from '$app/navigation';
	import { User, LogIn, Link2, BookOpen, Menu, X } from 'lucide-svelte';
	import { slide } from 'svelte/transition';

	const auth = getAuth();
	let menuOpen = $state(false);

	afterNavigate(() => {
		menuOpen = false;
	});
</script>

<header
	class="fixed top-0 right-0 left-0 z-50 border-b border-zinc-800/50 bg-zinc-950/80 backdrop-blur-xl"
>
	<div class="mx-auto flex max-w-3xl items-center justify-between px-4 py-4 sm:px-6">
		<a href="/" class="text-lg font-semibold tracking-tight text-zinc-50">URLinsight</a>

		<!-- Desktop nav -->
		<div class="hidden items-center gap-2 md:flex">
			{#if auth.isAuthenticated}
				<a
					href="/links"
					class="flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-zinc-400 transition-colors hover:bg-zinc-900 hover:text-zinc-50"
				>
					<Link2 class="h-4 w-4" />
					My Links
				</a>
				<a
					href="/profile"
					class="flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-zinc-400 transition-colors hover:bg-zinc-900 hover:text-zinc-50"
				>
					<User class="h-4 w-4" />
					Profile
				</a>
			{:else if !auth.loading}
				<a
					href="/login"
					class="flex items-center gap-2 rounded-lg border border-zinc-800 px-3 py-2 text-sm font-medium text-zinc-400 transition-colors hover:border-zinc-700 hover:text-zinc-50"
				>
					<LogIn class="h-4 w-4" />
					Sign in
				</a>
			{/if}
			<a
				href="/docs"
				class="flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-zinc-400 transition-colors hover:bg-zinc-900 hover:text-zinc-50"
			>
				<BookOpen class="h-4 w-4" />
				API
			</a>
		</div>

		<!-- Mobile burger -->
		<button
			onclick={() => (menuOpen = !menuOpen)}
			class="rounded-lg p-2 text-zinc-400 transition-colors hover:bg-zinc-900 hover:text-zinc-50 md:hidden"
			aria-label={menuOpen ? 'Close menu' : 'Open menu'}
		>
			{#if menuOpen}
				<X class="h-5 w-5" />
			{:else}
				<Menu class="h-5 w-5" />
			{/if}
		</button>
	</div>

	<!-- Mobile menu -->
	{#if menuOpen}
		<nav
			class="border-t border-zinc-800/50 px-4 pb-4 md:hidden"
			transition:slide={{ duration: 200 }}
		>
			<div class="flex flex-col gap-1 pt-2">
				{#if auth.isAuthenticated}
					<a
						href="/links"
						class="flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium text-zinc-300 transition-colors hover:bg-zinc-900 hover:text-zinc-50"
					>
						<Link2 class="h-4 w-4" />
						My Links
					</a>
					<a
						href="/profile"
						class="flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium text-zinc-300 transition-colors hover:bg-zinc-900 hover:text-zinc-50"
					>
						<User class="h-4 w-4" />
						Profile
					</a>
				{:else if !auth.loading}
					<a
						href="/login"
						class="flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium text-zinc-300 transition-colors hover:bg-zinc-900 hover:text-zinc-50"
					>
						<LogIn class="h-4 w-4" />
						Sign in
					</a>
				{/if}
				<a
					href="/docs"
					class="flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium text-zinc-300 transition-colors hover:bg-zinc-900 hover:text-zinc-50"
				>
					<BookOpen class="h-4 w-4" />
					API Docs
				</a>
			</div>
		</nav>
	{/if}
</header>
