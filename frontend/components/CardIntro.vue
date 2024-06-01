<template>
  <div class="flex items-center justify-between w-full p-10 bg-black bg-opacity-75 rounded-lg">
    <div class="flex items-center gap-4">
      <img src="~/assets/img/radiollama.jpg" alt="RadioLlama" class="rounded-lg" width="200" height="200"/>
      <div class="flex flex-col gap-2">
        <h1 class="text-2xl font-bold">RadioLlama</h1>
        <p class="text-sm">by Artist Name</p>
        <div class="flex items-center gap-4">
          <Button :label="playing ? 'STOP' : 'PLAY'" rounded severity="primary" @click="launchAudioTest"/>
          <!-- try it out redirect page /welcome -->
          <Button label="TRY IT OUT" rounded severity="primary" @click="$router.push('/welcome')"/>
        </div>
      </div>
    </div>  
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Button from 'primevue/button';

const playing = ref(false);
let audio: HTMLAudioElement | null = null;

// Get the path to the audio file
const audioPath = new URL('~/assets/audio/test.wav', import.meta.url).href;

const launchAudioTest = () => {
  if (playing.value) {
    // Stop the audio
    audio?.pause();
    audio = null;
    playing.value = false;
  } else {
    // Play the audio
    audio = new Audio(audioPath);
    audio.play();
    playing.value = true;

    // Reset playing state when audio ends
    audio.onended = () => {
      playing.value = false;
      audio = null;
    };
  }
};
</script>
