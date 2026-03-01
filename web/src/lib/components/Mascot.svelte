<script lang="ts">
	let { size = 120, animate = false }: { size?: number; animate?: boolean } = $props();
</script>

<svg
	width={size}
	height={size}
	viewBox="0 0 16 16"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
	role="img"
	aria-label="URLinsight mascot"
	style="image-rendering: pixelated;"
>
	<!-- Body -->
	<rect x="4" y="5" width="8" height="7" fill="#3f3f46" />
	<rect x="5" y="4" width="6" height="1" fill="#3f3f46" />
	<rect x="5" y="12" width="6" height="1" fill="#3f3f46" />

	<!-- Eyes -->
	<rect x="5" y="7" width="2" height="2" fill="#a1a1aa" />
	<rect x="9" y="7" width="2" height="2" fill="#a1a1aa" />
	<rect x="6" y="7" width="1" height="1" fill="#fafafa" />
	<rect x="10" y="7" width="1" height="1" fill="#fafafa" />

	<!-- Mouth -->
	<rect x="6" y="10" width="4" height="1" fill="#71717a" />

	<!-- Antenna (chain link) -->
	<rect x="7" y="1" width="2" height="1" fill="#71717a" />
	<rect x="6" y="2" width="1" height="2" fill="#71717a" />
	<rect x="9" y="2" width="1" height="2" fill="#71717a" />
	<rect x="7" y="3" width="2" height="1" fill="#a1a1aa" />

	<!-- Left hand -->
	<g>
		<rect x="2" y="7" width="2" height="1" fill="#52525b" />
		<rect x="2" y="8" width="1" height="1" fill="#52525b" />
		{#if animate}
			<animateTransform
				attributeName="transform"
				type="rotate"
				values="0 3 8;-15 3 8;0 3 8;0 3 8"
				dur="2s"
				repeatCount="indefinite"
			/>
		{/if}
	</g>

	<!-- Right hand (waving) -->
	<g>
		<rect x="12" y="7" width="2" height="1" fill="#52525b" />
		<rect x="13" y="6" width="1" height="1" fill="#52525b" />
		{#if animate}
			<animateTransform
				attributeName="transform"
				type="rotate"
				values="0 13 8;20 13 8;-10 13 8;0 13 8"
				dur="1.2s"
				repeatCount="indefinite"
			/>
		{/if}
	</g>

	<!-- Feet -->
	<rect x="5" y="13" width="2" height="1" fill="#52525b" />
	<rect x="9" y="13" width="2" height="1" fill="#52525b" />

	<!-- Blink animation overlay -->
	{#if animate}
		<rect x="5" y="7" width="2" height="2" fill="#3f3f46">
			<animate attributeName="opacity" values="0;0;1;0;0" dur="3s" keyTimes="0;0.28;0.3;0.32;1" repeatCount="indefinite" />
		</rect>
		<rect x="9" y="7" width="2" height="2" fill="#3f3f46">
			<animate attributeName="opacity" values="0;0;1;0;0" dur="3s" keyTimes="0;0.28;0.3;0.32;1" repeatCount="indefinite" />
		</rect>
	{/if}
</svg>
