<script lang="ts">
	import { onMount } from 'svelte';

	let { size = 120, animate = false }: { size?: number; animate?: boolean } = $props();

	let svgEl: SVGSVGElement | undefined = $state();
	let pupilX = $state(0);
	let pupilY = $state(0);

	onMount(() => {
		let targetX = 0;
		let targetY = 0;

		function handleMouseMove(e: MouseEvent) {
			if (!svgEl) return;
			const rect = svgEl.getBoundingClientRect();
			const cx = rect.left + rect.width / 2;
			const cy = rect.top + rect.height / 2;

			const dx = e.clientX - cx;
			const dy = e.clientY - cy;
			const dist = Math.sqrt(dx * dx + dy * dy);
			const max = 0.5;

			if (dist > 1) {
				const t = Math.min(dist / 150, 1);
				targetX = (dx / dist) * max * t;
				targetY = (dy / dist) * max * t;
			} else {
				targetX = 0;
				targetY = 0;
			}
		}

		let frameId: number;
		function tick() {
			pupilX += (targetX - pupilX) * 0.12;
			pupilY += (targetY - pupilY) * 0.12;
			frameId = requestAnimationFrame(tick);
		}

		window.addEventListener('mousemove', handleMouseMove);
		frameId = requestAnimationFrame(tick);

		return () => {
			window.removeEventListener('mousemove', handleMouseMove);
			cancelAnimationFrame(frameId);
		};
	});
</script>

<svg
	bind:this={svgEl}
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
	<rect x="4" y="5" width="8" height="7" fill="#73AB84" />
	<rect x="5" y="4" width="6" height="1" fill="#73AB84" />
	<rect x="5" y="12" width="6" height="1" fill="#73AB84" />

	<!-- Belly highlight -->
	<rect x="6" y="9" width="4" height="2" fill="#93c9a2" />

	<!-- Eye sockets -->
	<rect x="5" y="7" width="2" height="2" fill="#4a90d9" />
	<rect x="9" y="7" width="2" height="2" fill="#4a90d9" />

	<!-- Pupils (follow mouse) -->
	<rect x={5.5 + pupilX} y={7.5 + pupilY} width="1" height="1" fill="#e0eeff" />
	<rect x={9.5 + pupilX} y={7.5 + pupilY} width="1" height="1" fill="#e0eeff" />

	<!-- Mouth -->
	<rect x="7" y="10" width="2" height="1" fill="#2d5e3f" />

	<!-- Antenna (chain link) -->
	<rect x="7" y="1" width="2" height="1" fill="#3d7252" />
	<rect x="6" y="2" width="1" height="2" fill="#3d7252" />
	<rect x="9" y="2" width="1" height="2" fill="#3d7252" />
	<rect x="7" y="3" width="2" height="1" fill="#93c9a2" />

	<!-- Left hand -->
	<g>
		<rect x="2" y="7" width="2" height="1" fill="#2d5e3f" />
		<rect x="2" y="8" width="1" height="1" fill="#2d5e3f" />
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
		<rect x="12" y="7" width="2" height="1" fill="#2d5e3f" />
		<rect x="13" y="6" width="1" height="1" fill="#2d5e3f" />
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
	<rect x="5" y="13" width="2" height="1" fill="#2d5e3f" />
	<rect x="9" y="13" width="2" height="1" fill="#2d5e3f" />

	<!-- Blink animation overlay -->
	{#if animate}
		<rect x="5" y="7" width="2" height="2" fill="#73AB84">
			<animate attributeName="opacity" values="0;0;1;0;0" dur="3s" keyTimes="0;0.28;0.3;0.32;1" repeatCount="indefinite" />
		</rect>
		<rect x="9" y="7" width="2" height="2" fill="#73AB84">
			<animate attributeName="opacity" values="0;0;1;0;0" dur="3s" keyTimes="0;0.28;0.3;0.32;1" repeatCount="indefinite" />
		</rect>
	{/if}
</svg>
