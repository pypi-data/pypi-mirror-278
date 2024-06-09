<script context="module" lang="ts">
    export { default as BaseModel4DGS } from "./shared/Model4DGS.svelte";
    export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
    import type { FileData } from "@gradio/client";
    import Model4DGS from "./shared/Model4DGS.svelte";
    import { BlockLabel, Block, Empty } from "@gradio/atoms";
    import { File } from "@gradio/icons";
    import { StatusTracker } from "@gradio/statustracker";
    import type { LoadingStatus } from "@gradio/statustracker";
    import type { Gradio } from "@gradio/utils";

    export let elem_id = "";
    export let elem_classes: string[] = [];
    export let visible = true;
    export let value: null | { files: FileData[]; } = null;
    export let root: string;
    export let proxy_url: null | string;
    export let loading_status: LoadingStatus;
    export let label: string;
    export let show_label: boolean;
    export let container = true;
    export let scale: number | null = null;
    export let min_width: number | undefined = undefined;
    export let gradio: Gradio;
    export let height: number | undefined = undefined;
    export let fps=8;

    let dragging = false;
</script>

<Block
    {visible}
    variant={value === null ? "dashed" : "solid"}
    border_mode={dragging ? "focus" : "base"}
    padding={false}
    {elem_id}
    {elem_classes}
    {container}
    {scale}
    {min_width}
    {height}
>
    <StatusTracker autoscroll={gradio.autoscroll} i18n={gradio.i18n} {...loading_status} />

    {#if value}
        <BlockLabel {show_label} Icon={File} label={label || "Splat"} />
        <Model4DGS
            bind:value
            i18n={gradio.i18n}
            {label}
            {show_label}
            {root}
            {proxy_url}
            {fps}
        />
    {:else}
        <BlockLabel {show_label} Icon={File} label={label || "Splat"} />

        <Empty unpadded_box={true} size="large"><File /></Empty>
    {/if}
</Block>
