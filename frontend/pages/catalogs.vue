<template>
    <div class="mb-20">
        <div class="grid grid-cols-12 ">
            <div class="flex flex-col col-span-10 col-start-2 gap-5">
                <div v-for="i in 5"
                    class="flex items-center justify-center md:justify-start w-full p-10 bg-black bg-opacity-75 rounded-lg">
                    <div class="flex flex-col md:flex-row items-center gap-10">
                        <div class="flex flex-col gap-2">
                            <h1 class="text-2xl font-bold">radio title</h1>
                            <div class="flex items-center gap-4">
                                <Button :icon="playing ? 'pi pi-pause' : 'pi pi-play'" :label="playing ? 'PAUSE' : 'PLAY'" rounded @click="launchAudioTest" />
                            </div>
                        </div>  
                    </div> 
                </div>
            </div>
        </div>
    </div>
</template>