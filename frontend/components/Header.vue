<template>
    <header class="flex items-center justify-between w-full p-10">
        <div>RadioLlama</div>
        <div class="flex items-center justify-between gap-4">
            <i class="pi pi-facebook"></i>
            <i class="pi pi-twitter"></i>
            <i class="pi pi-linkedin"></i>
        </div>
        <div>
            <Button v-if="visible" label="LOG IN" rounded severity="help" @click="$router.push('/login')"/>
        </div>
    </header>
</template>

<script setup lang="ts">
import Button from 'primevue/button';
import { useRouter } from 'vue-router';
const router = useRouter();
const visible = router.currentRoute.value.name !== 'login';
</script>