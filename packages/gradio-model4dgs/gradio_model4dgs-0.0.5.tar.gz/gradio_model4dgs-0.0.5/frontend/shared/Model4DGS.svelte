<script lang="ts">
    import { FileData, normalise_file } from "@gradio/client";
    import { BlockLabel } from "@gradio/atoms";
    import { File } from "@gradio/icons";
    import { onMount } from "svelte";
    import * as GaussianSplats3D from "@mkkellogg/gaussian-splats-3d";
    import * as THREE from "three";
    import type { I18nFormatter } from "@gradio/utils";

    export let value: null | { files: FileData[]; };
    export let root: string;
    export let proxy_url: null | string;
    export let label = "";
    export let show_label: boolean;
    export let i18n: I18nFormatter;
    export let fps=8;


    let currFrameIndex = 0;
    let NUM_FRAMES = 1;
    
    var sceneOptions: Array<object> = []
    const visible_scale = new THREE.Vector3(1.25, 1.25, 1.25);
    const invisible_scale = new THREE.Vector3(0.01, 0.01, 0.01);

    onMount(() => {
        if (value != null && value.files != null) {    
            const viewerContainer = document.querySelector('.model4DGS');
            const viewer = new GaussianSplats3D.Viewer({
                cameraUp: [0, 1, 0],
                initialCameraPosition: [0, 0, 4],
                initialCameraLookAt: [0, 0, -1],
                dynamicScene: true,
                sharedMemoryForWorkers: false,
                rootElement: viewerContainer
            });

            NUM_FRAMES = value.files.length;
            let files = value.files;

            for (let i = 0; i < files.length; i++) {
                let opt = {
                    path: normalise_file(files[i], root, proxy_url).url,
                    scale: [invisible_scale, invisible_scale, invisible_scale]
                };
                sceneOptions.push(opt);
            }

            viewer
                .addSplatScenes(sceneOptions,true)
                .then(() => {
                    viewer.start();

                    let startTime = performance.now();
                    requestAnimationFrame(update);
                    function update() {
                        requestAnimationFrame(update);
                        const timeDelta = performance.now() - startTime;

                        if (timeDelta > 1000/fps) {
                            const prevSplatScene = viewer.getSplatScene(currFrameIndex);
                            prevSplatScene.scale.copy(invisible_scale);

                            startTime = performance.now();
                            currFrameIndex++;
                            if (currFrameIndex >= NUM_FRAMES) currFrameIndex = 0;

                            const curSplatScene = viewer.getSplatScene(currFrameIndex);
                            curSplatScene.scale.copy(visible_scale);
                        }
                    }
                });
        }
    });
</script>

<BlockLabel {show_label} Icon={File} label={label || i18n("4DGS_model.splat")} />
<div class="model4DGS">
</div>

<style>
    .model4DGS {
        display: flex;
        position: relative;
        width: var(--size-full);
        height: var(--size-full);
        min-height: 250px;
    }
</style>

