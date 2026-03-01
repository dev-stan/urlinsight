<script lang="ts">
	import { onMount } from 'svelte';
	import { getAuth } from '$lib/auth.svelte';
	import Header from '$lib/components/Header.svelte';
	import { ArrowRight, Lock, Globe, BarChart3, UserPlus } from 'lucide-svelte';

	const auth = getAuth();
	onMount(() => auth.init());

	const examples = {
		curlBody: '{"target_url": "https://example.com"}',
		linkResponse: '{"short_code": "Ab3xK9", "target_url": "https://example.com"}',
		registerBody: '{"email": "user@example.com", "password": "your_password"}',
		userResponse: '{"id": 1, "email": "user@example.com"}',
		tokenResponse: '{"access_token": "eyJ...", "token_type": "bearer"}',
		passwordBody: '{"current_password": "old_pass", "new_password": "new_pass"}',
		passwordResponse: '{"detail": "Password updated"}',
		linksListResponse: '[{"short_code": "Ab3xK9", "target_url": "https://example.com"}]',
		analyticsResponse: `{
  "short_code": "Ab3xK9",
  "target_url": "https://example.com",
  "totals": {
    "clicks": 42,
    "unique_visitors": 31
  },
  "daily": [
    {"date": "2025-03-01", "clicks": 10, "unique_visitors": 8}
  ]
}`
	};
</script>

<svelte:head>
	<title>Docs - URLinsight</title>
</svelte:head>

<Header />

<main class="pt-24 pb-20">
	<div class="mx-auto max-w-2xl px-6">
		<h1 class="mb-2 text-2xl font-semibold text-zinc-50">API Documentation</h1>
		<p class="mb-10 text-sm text-zinc-500">
			Base URL: <code class="rounded bg-zinc-800 px-1.5 py-0.5 text-zinc-300">http://localhost:8000</code>
		</p>

		<!-- Quick start -->
		<section class="mb-10">
			<h2 class="mb-4 text-lg font-semibold text-zinc-50">Quick Start</h2>
			<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5 text-sm">
				<p class="mb-3 text-zinc-400">Shorten a URL with a single request:</p>
				<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-4 text-zinc-300"><code>curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{examples.curlBody}'</code></pre>
				<p class="mt-3 text-zinc-500">Response:</p>
				<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-4 text-zinc-300"><code>{examples.linkResponse}</code></pre>
			</div>
		</section>

		<!-- Auth endpoints -->
		<section class="mb-10">
			<div class="mb-4 flex items-center gap-2">
				<UserPlus class="h-5 w-5 text-zinc-400" />
				<h2 class="text-lg font-semibold text-zinc-50">Authentication</h2>
			</div>

			<div class="space-y-4">
				<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
					<div class="mb-2 flex items-center gap-2">
						<span class="rounded bg-emerald-900/50 px-2 py-0.5 text-xs font-semibold text-emerald-400">POST</span>
						<code class="text-sm text-zinc-200">/auth/register</code>
					</div>
					<p class="mb-3 text-sm text-zinc-500">Create a new account. Links created while authenticated are saved to your profile.</p>
					<div class="space-y-2 text-sm">
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Request body</p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.registerBody}</code></pre>
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Response <span class="text-zinc-700">200</span></p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.userResponse}</code></pre>
						<p class="text-xs text-zinc-600"><span class="text-red-400/70">409</span> — Email already registered</p>
					</div>
				</div>

				<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
					<div class="mb-2 flex items-center gap-2">
						<span class="rounded bg-emerald-900/50 px-2 py-0.5 text-xs font-semibold text-emerald-400">POST</span>
						<code class="text-sm text-zinc-200">/auth/login</code>
					</div>
					<p class="mb-3 text-sm text-zinc-500">Get a JWT access token.</p>
					<div class="space-y-2 text-sm">
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Request body</p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.registerBody}</code></pre>
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Response <span class="text-zinc-700">200</span></p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.tokenResponse}</code></pre>
						<p class="text-xs text-zinc-600"><span class="text-red-400/70">401</span> — Invalid email or password</p>
					</div>
				</div>

				<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
					<div class="mb-2 flex items-center gap-2">
						<span class="rounded bg-blue-900/50 px-2 py-0.5 text-xs font-semibold text-blue-400">GET</span>
						<code class="text-sm text-zinc-200">/auth/me</code>
						<Lock class="h-3.5 w-3.5 text-zinc-600" />
					</div>
					<p class="mb-3 text-sm text-zinc-500">Get the current authenticated user.</p>
					<div class="space-y-2 text-sm">
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Headers</p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>Authorization: Bearer &lt;token&gt;</code></pre>
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Response <span class="text-zinc-700">200</span></p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.userResponse}</code></pre>
					</div>
				</div>

				<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
					<div class="mb-2 flex items-center gap-2">
						<span class="rounded bg-amber-900/50 px-2 py-0.5 text-xs font-semibold text-amber-400">PUT</span>
						<code class="text-sm text-zinc-200">/auth/password</code>
						<Lock class="h-3.5 w-3.5 text-zinc-600" />
					</div>
					<p class="mb-3 text-sm text-zinc-500">Change your password.</p>
					<div class="space-y-2 text-sm">
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Request body</p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.passwordBody}</code></pre>
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Response <span class="text-zinc-700">200</span></p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.passwordResponse}</code></pre>
						<p class="text-xs text-zinc-600"><span class="text-red-400/70">401</span> — Current password is incorrect</p>
					</div>
				</div>
			</div>
		</section>

		<!-- Links endpoints -->
		<section class="mb-10">
			<div class="mb-4 flex items-center gap-2">
				<Globe class="h-5 w-5 text-zinc-400" />
				<h2 class="text-lg font-semibold text-zinc-50">Links</h2>
			</div>

			<div class="space-y-4">
				<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
					<div class="mb-2 flex items-center gap-2">
						<span class="rounded bg-emerald-900/50 px-2 py-0.5 text-xs font-semibold text-emerald-400">POST</span>
						<code class="text-sm text-zinc-200">/links</code>
					</div>
					<p class="mb-3 text-sm text-zinc-500">Shorten a URL. Auth is optional — if authenticated, the link is saved to your account.</p>
					<div class="space-y-2 text-sm">
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Request body</p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.curlBody}</code></pre>
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Response <span class="text-zinc-700">200</span></p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.linkResponse}</code></pre>
					</div>
				</div>

				<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
					<div class="mb-2 flex items-center gap-2">
						<span class="rounded bg-blue-900/50 px-2 py-0.5 text-xs font-semibold text-blue-400">GET</span>
						<code class="text-sm text-zinc-200">/links</code>
						<Lock class="h-3.5 w-3.5 text-zinc-600" />
					</div>
					<p class="mb-3 text-sm text-zinc-500">List all links belonging to the authenticated user.</p>
					<div class="space-y-2 text-sm">
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Response <span class="text-zinc-700">200</span></p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.linksListResponse}</code></pre>
						<p class="text-xs text-zinc-600"><span class="text-red-400/70">401</span> — Not authenticated</p>
					</div>
				</div>

				<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
					<div class="mb-2 flex items-center gap-2">
						<span class="rounded bg-blue-900/50 px-2 py-0.5 text-xs font-semibold text-blue-400">GET</span>
						<code class="text-sm text-zinc-200">/links/:short_code</code>
					</div>
					<p class="mb-3 text-sm text-zinc-500">Get details for a specific link by its short code.</p>
					<div class="space-y-2 text-sm">
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Response <span class="text-zinc-700">200</span></p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.linkResponse}</code></pre>
						<p class="text-xs text-zinc-600"><span class="text-red-400/70">404</span> — Link not found</p>
					</div>
				</div>
			</div>
		</section>

		<!-- Analytics endpoints -->
		<section class="mb-10">
			<div class="mb-4 flex items-center gap-2">
				<BarChart3 class="h-5 w-5 text-zinc-400" />
				<h2 class="text-lg font-semibold text-zinc-50">Analytics</h2>
			</div>

			<div class="space-y-4">
				<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
					<div class="mb-2 flex items-center gap-2">
						<span class="rounded bg-blue-900/50 px-2 py-0.5 text-xs font-semibold text-blue-400">GET</span>
						<code class="text-sm text-zinc-200">/links/:short_code/analytics</code>
					</div>
					<p class="mb-3 text-sm text-zinc-500">Get click and unique visitor analytics for a link, including daily breakdowns.</p>
					<div class="space-y-2 text-sm">
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Response <span class="text-zinc-700">200</span></p>
						<pre class="overflow-x-auto rounded-lg bg-zinc-950 p-3 text-zinc-300"><code>{examples.analyticsResponse}</code></pre>
					</div>
				</div>
			</div>
		</section>

		<!-- Redirect -->
		<section class="mb-10">
			<div class="mb-4 flex items-center gap-2">
				<ArrowRight class="h-5 w-5 text-zinc-400" />
				<h2 class="text-lg font-semibold text-zinc-50">Redirect</h2>
			</div>

			<div class="space-y-4">
				<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
					<div class="mb-2 flex items-center gap-2">
						<span class="rounded bg-blue-900/50 px-2 py-0.5 text-xs font-semibold text-blue-400">GET</span>
						<code class="text-sm text-zinc-200">/redirect/:short_code</code>
					</div>
					<p class="mb-3 text-sm text-zinc-500">Redirects to the target URL. Automatically records a click event and tracks unique visitors by hashed IP.</p>
					<div class="space-y-2 text-sm">
						<p class="text-xs font-medium uppercase tracking-wide text-zinc-600">Response <span class="text-zinc-700">302</span></p>
						<p class="text-xs text-zinc-400">Redirects to the original URL</p>
						<p class="text-xs text-zinc-600"><span class="text-red-400/70">404</span> — Link not found</p>
					</div>
				</div>
			</div>
		</section>

		<!-- Rate limiting -->
		<section>
			<h2 class="mb-4 text-lg font-semibold text-zinc-50">Rate Limiting</h2>
			<div class="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5 text-sm text-zinc-400">
				<p>All endpoints are rate-limited via Redis. If you exceed the limit, you'll receive a <code class="rounded bg-zinc-800 px-1 py-0.5 text-zinc-300">429 Too Many Requests</code> response.</p>
			</div>
		</section>
	</div>
</main>
