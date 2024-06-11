<script lang="ts">
	import { BlockLabel, Empty, ShareButton } from "@gradio/atoms";
	import { BaseButton } from "@gradio/button";
	import { Image as ImageIcon } from "@gradio/icons";
	import { Loader } from "@gradio/statustracker";
	import type { I18nFormatter, SelectData, ShareData } from "@gradio/utils";
	import { dequal } from "dequal";
	import { createEventDispatcher, tick } from "svelte";

	import Image from "./Image.svelte";
	import {
		type Breakpoints,
		breakpoints,
		copy_to_clipboard,
		format_gallery_for_sharing,
		type GalleryData,
		GalleryImage,
	} from "./utils";

	export let object_fit:
		| "contain"
		| "cover"
		| "fill"
		| "none"
		| "scale-down" = "cover";
	export let show_label = true;
	export let has_more = false;
	export let label: string;
	export let pending: boolean;
	export let value: GalleryData | null = null;
	export let columns: number | number[] | Breakpoints | undefined = [2];
	export let height: number | "auto" = "auto";
	export let preview: boolean = false;
	export let proxy_url: string;
	export let allow_preview = false;
	export let show_share_button = false;
	export let deletable: boolean;
	export let show_download_button = false;
	export let i18n: I18nFormatter;
	export let selected_index: number | null = null;
	export let load_more_button_props: Record<string, any> = {};
	let breakpointColumns: [breakpoint: number, column: number][] = [];
	let cols: number;
	let client_height = 0;
	let window_height = 0;
	let window_width = 0;
	$: {
		if (typeof columns === "object" && columns !== null) {
			if (Array.isArray(columns)) {
				const columns_len = columns.length;
				breakpointColumns = breakpoints.map((breakpoint, i) => {
					return [
						breakpoint.width,
						(columns as number[])[i] ??
							(columns as number[])[columns_len - 1],
					];
				});
			} else {
				let last_column = 0;
				breakpointColumns = breakpoints.map((breakpoint) => {
					const column = (columns as Breakpoints)[breakpoint.key];
					last_column = column ?? last_column;
					return [breakpoint.width, last_column];
				});
			}
		} else {
			breakpointColumns = breakpoints.map((breakpoint) => {
				return [breakpoint.width, columns as number];
			});
		}
	}

	const dispatch = createEventDispatcher<{
		change: void;
		select: SelectData;
		load_more: void;
		delete_image: GalleryImage;
		click: Omit<SelectData, "selected">;
		share: ShareData;
		error: string;
	}>();

	$: {
		for (const [breakpoint, column] of [...breakpointColumns].reverse()) {
			if (window_width >= breakpoint) {
				cols = column;
				break;
			}
		}
	}

	// tracks whether the value of the gallery was reset
	let was_reset = true;

	$: was_reset = value == null || value.length === 0 ? true : was_reset;

	let resolved_value: GalleryData | null = null;
	$: resolved_value =
		value == null
			? null
			: value.map((item) => {
					return item;
				});
	let prev_value: GalleryData | null = value;

	if (selected_index == null && preview && value?.length) {
		selected_index = 0;
	}
	let old_selected_index: number | null = selected_index;

	$: if (!dequal(prev_value, value)) {
		// If value is falsy (clear button or first load), preview determines the selected image
		if (was_reset) {
			selected_index =
				preview && value?.length ? selected_index ?? 0 : null;
			was_reset = false;
		} else {
			selected_index =
				selected_index != null &&
				value != null &&
				selected_index < value.length
					? selected_index
					: null;
		}
		dispatch("change");
		prev_value = value;
	}

	$: previous =
		((selected_index ?? 0) + (resolved_value?.length ?? 0) - 1) %
		(resolved_value?.length ?? 0);
	$: next = ((selected_index ?? 0) + 1) % (resolved_value?.length ?? 0);

	function handle_preview_click(event: MouseEvent): void {
		const element = event.target as HTMLElement;
		const x = event.clientX;
		const width = element.offsetWidth;
		const centerX = width / 2;

		if (x < centerX) {
			selected_index = previous;
		} else {
			selected_index = next;
		}
	}

	function handleDeleteImage(event) {
		dispatch("delete_image", event.detail.image.orig_name);
	}

	function on_keydown(e: KeyboardEvent): void {
		switch (e.code) {
			case "Escape":
				e.preventDefault();
				break;
			case "ArrowLeft":
				e.preventDefault();
				selected_index = previous;
				break;
			case "ArrowRight":
				e.preventDefault();
				selected_index = next;
				break;
			default:
				break;
		}
	}

	$: {
		if (selected_index !== old_selected_index) {
			old_selected_index = selected_index;
			if (selected_index !== null) {
				dispatch("select", {
					index: selected_index,
					value: resolved_value?.[selected_index],
				});
			}
		}
	}

	$: if (allow_preview) {
		scroll_to_img(selected_index);
	}

	let el: HTMLButtonElement[] = [];
	let container_element: HTMLDivElement;

	async function scroll_to_img(index: number | null): Promise<void> {
		if (typeof index !== "number") return;
		await tick();

		if (el[index] === undefined) return;

		el[index]?.focus();

		const { left: container_left, width: container_width } =
			container_element.getBoundingClientRect();
		const { left, width } = el[index].getBoundingClientRect();

		const relative_left = left - container_left;

		const pos =
			relative_left +
			width / 2 -
			container_width / 2 +
			container_element.scrollLeft;

		if (
			container_element &&
			typeof container_element.scrollTo === "function"
		) {
			container_element.scrollTo({
				left: pos < 0 ? 0 : pos,
				behavior: "smooth",
			});
		}
	}

	$: selected_image =
		selected_index != null && resolved_value != null
			? resolved_value[selected_index]
			: null;
</script>

<svelte:window
	bind:innerHeight={window_height}
	bind:innerWidth={window_width}
/>

{#if show_label}
	<BlockLabel {show_label} Icon={ImageIcon} label={label || "Gallery"} />
{/if}
{#if !value || !resolved_value || resolved_value.length === 0}
	<Empty unpadded_box={true} size="large"><ImageIcon /></Empty>
{:else}
	{#if selected_image && allow_preview}
		<button on:keydown={on_keydown} class="preview">
			<button
				class="image-button"
				on:click={(event) => handle_preview_click(event)}
				style="height: calc(100% - {selected_image.caption
					? '80px'
					: '60px'})"
				aria-label="detailed view of selected image"
			>
				<img
					data-testid="detailed-image"
					src={selected_image.image.url}
					alt={selected_image.caption || ""}
					title={selected_image.caption || null}
					class:with-caption={!!selected_image.caption}
					loading="lazy"
				/>
			</button>

			{#if selected_image?.caption}
				<caption class="caption">
					{selected_image.caption}
				</caption>
			{/if}

			<div
				bind:this={container_element}
				class="thumbnails scroll-hide"
				data-testid="container_el"
			>
				{#each resolved_value as entry, i}
					<button
						bind:this={el[i]}
						on:click={() => (selected_index = i)}
						class="thumbnail-item thumbnail-small"
						class:selected={selected_index === i}
						aria-label={"Thumbnail " +
							(i + 1) +
							" of " +
							resolved_value.length}
					>
						<img
							src={entry.image.url}
							title={entry.caption || null}
							data-testid={"thumbnail " + (i + 1)}
							alt=""
							loading="lazy"
						/>
					</button>
				{/each}
			</div>
		</button>
	{/if}
	<div
		bind:clientHeight={client_height}
		class="grid-wrap"
		class:fixed-height={!height || height === "auto"}
		style="height: {height}px;"
	>
		<div
			class="grid-container"
			style="--object-fit: {object_fit}; min-height: {height}px;"
			class:pt-6={show_label}
		>
			{#if show_share_button}
				<div class="icon-button">
					<ShareButton
						{i18n}
						on:share={(e) => {
							copy_to_clipboard(e.detail.description);
						}}
						on:error
						value={resolved_value}
						formatter={format_gallery_for_sharing}
					/>
				</div>
			{/if}
			<div>
				{#each resolved_value as entry, i}
					<div
						class="thumbnail-item thumbnail-lg"
						class:selected={selected_index === i}
						aria-label={"Thumbnail " +
							(i + 1) +
							" of " +
							resolved_value.length}
					>
						<Image
							{deletable}
							value={entry}
							on:click={() => (selected_index = i)}
							on:delete_image={(imageToDelete) =>
								handleDeleteImage(imageToDelete)}
						/>
					</div>
				{/each}
			</div>
		</div>
		<p
			class="loading-line"
			class:visible={!(selected_image && allow_preview) && has_more}
		>
			{#if pending}
				<Loader margin={false} />
			{:else}
				<BaseButton
					{...load_more_button_props}
					on:click={() => {
						dispatch("load_more");
					}}
				>
					{i18n(
						load_more_button_props.value ||
							load_more_button_props.label ||
							"Load More",
					)}</BaseButton
				>
			{/if}
		</p>
	</div>
{/if}

<style lang="postcss">
	.preview {
		display: flex;
		position: absolute;
		top: 0px;
		right: 0px;
		bottom: 0px;
		left: 0px;
		flex-direction: column;
		z-index: var(--layer-2);
		backdrop-filter: blur(8px);
		background: var(--background-fill-primary);
		height: var(--size-full);
	}
	.loading-line {
		display: none;
	}
	.loading-line.visible {
		margin-top: 20px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.fixed-height {
		min-height: var(--size-80);
		max-height: 55vh;
	}

	@media (--screen-xl) {
		.fixed-height {
			min-height: 450px;
		}
	}

	.image-button {
		height: calc(100% - 60px);
		width: 100%;
		display: flex;
	}
	.preview img {
		width: var(--size-full);
		height: var(--size-full);
		object-fit: contain;
	}

	.preview img.with-caption {
		height: var(--size-full);
	}

	.caption {
		padding: var(--size-2) var(--size-3);
		overflow: hidden;
		color: var(--block-label-text-color);
		font-weight: var(--weight-semibold);
		text-align: center;
		text-overflow: ellipsis;
		white-space: nowrap;
		align-self: center;
	}

	.thumbnails {
		display: flex;
		position: absolute;
		bottom: 0;
		justify-content: center;
		align-items: center;
		gap: var(--spacing-lg);
		width: var(--size-full);
		height: var(--size-14);
		overflow-x: scroll;
	}

	.thumbnail-item {
		break-inside: avoid;
		box-shadow:
			0 0 0 2px var(--ring-color),
			var(--shadow-drop);
		border-radius: var(--button-small-radius);
		background: var(--background-fill-secondary);
		overflow: clip;
	}

	.thumbnail-item.selected {
		--ring-color: var(--color-accent);
	}

	.thumbnail-small {
		flex: none;
		transform: scale(0.9);
		transition: 0.075s;
		width: var(--size-9);
		height: var(--size-9);
	}

	.thumbnail-small.selected {
		--ring-color: var(--color-accent);
		transform: scale(1);
		border-color: var(--color-accent);
	}

	.thumbnail-small > img {
		width: var(--size-full);
		overflow: hidden;
		object-fit: var(--object-fit);
	}

	.grid-wrap {
		position: relative;
		padding: var(--size-2);
		height: var(--size-full);
		overflow-y: scroll;
		box-sizing: content-box;
	}

	.grid-container {
		gap: var(--spacing-lg);
	}

	.icon-button {
		position: absolute;
		top: 0px;
		right: 0px;
		z-index: var(--layer-2);
	}
</style>
