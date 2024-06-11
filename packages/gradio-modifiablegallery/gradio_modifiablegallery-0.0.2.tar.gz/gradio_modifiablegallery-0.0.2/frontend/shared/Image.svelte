<svelte:options accessors={true} />

<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import type { GalleryImage } from "./utils";

  const dispatch = createEventDispatcher<{
    click: void;
    delete_image: GalleryImage;
  }>();
  export let deletable: boolean;
  export let value: GalleryImage;
</script>

<div class="thumbnail-image-box">
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
  <img
    on:click={() => dispatch("click")}
    alt={value.caption || ""}
    src={value.image.url}
    class="thumbnail-img"
    loading="lazy"
  />

  {#if value.caption}
    <div class="foot-label left-label">
      {value.caption}
    </div>
  {/if}

  {#if deletable}
    <button
      class="delete-button"
      on:click={() => {
        dispatch("delete_image", value);
      }}
      ><svg
        width="15"
        height="15"
        viewBox="0 0 16 16"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="8" cy="8" r="8" fill="#FF6700" />
        <path
          d="M11.5797 10.6521C11.8406 10.913 11.8406 11.3188 11.5797 11.5797C11.4492 11.7101 11.2898 11.7681 11.1159 11.7681C10.942 11.7681 10.7826 11.7101 10.6521 11.5797L7.99997 8.92751L5.3478 11.5797C5.21736 11.7101 5.05794 11.7681 4.88403 11.7681C4.71012 11.7681 4.5507 11.7101 4.42026 11.5797C4.15939 11.3188 4.15939 10.913 4.42026 10.6521L7.07244 7.99997L4.42026 5.3478C4.15939 5.08693 4.15939 4.68113 4.42026 4.42026C4.68113 4.15939 5.08693 4.15939 5.3478 4.42026L7.99997 7.07244L10.6521 4.42026C10.913 4.15939 11.3188 4.15939 11.5797 4.42026C11.8406 4.68113 11.8406 5.08693 11.5797 5.3478L8.92751 7.99997L11.5797 10.6521Z"
          fill="#FFF4EA"
        />
      </svg>
    </button>
  {/if}
</div>

<style>
  .thumbnail-image-box {
    width: 100%;
    height: 100%;
    overflow: hidden;
    position: relative;
  }
  .thumbnail-image-box:hover .left-label {
    opacity: 0.5;
  }

  .delete-button {
    position: absolute;
    right: var(--block-label-margin);
    top: var(--block-label-margin);
    z-index: var(--layer-1);
    display: flex;
    margin: 10px;
  }

  .foot-label {
    position: absolute;
    /* left: 0; */
    /* right: var(--block-label-margin); */
    bottom: var(--block-label-margin);
    z-index: var(--layer-1);
    border-top: 1px solid var(--border-color-primary);
    border-left: 1px solid var(--border-color-primary);

    background: var(--background-fill-secondary);
    padding: var(--block-label-padding);
    max-width: 80%;
    overflow: hidden;
    font-size: var(--block-label-text-size);
    text-align: left;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .left-label {
    left: 0;
    border-radius: 0 calc(var(--radius-lg) - 1px) 0 calc(var(--radius-lg) - 1px);
  }
  .right-label {
    right: var(--block-label-margin);
    border-radius: calc(var(--radius-lg) - 1px) 0 calc(var(--radius-lg) - 1px) 0;
  }

  .thumbnail-img {
    cursor: pointer;
    width: var(--size-full);
    overflow: hidden;
    object-fit: var(--object-fit);
    transition: transform 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
  }

  @keyframes shine {
    0% {
      background-position: -200px 0;
    }
    100% {
      background-position: 200px 0;
    }
  }
</style>
