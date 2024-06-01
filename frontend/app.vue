<template>
  <div class="card flex justify-center">
    hello ?
    <Sidebar v-model:visible="visible" header="Sidebar">
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
    </Sidebar>

    <Button icon="pi pi-arrow-right" @click="visible = true" />
  </div>
</template>

<script setup lang="ts">
import 'primevue/resources/themes/aura-light-green/theme.css'

import Sidebar from 'primevue/sidebar';
import Button from 'primevue/button';

import { ref } from 'vue';
const visible = ref(false);
</script>