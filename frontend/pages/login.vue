<template>
    <div class="grid grid-cols-12 gap-4 p-10">
        <div class="flex flex-col col-start-2 col-span-10 gap-10">
            <div class="flex flex-col items-start gap-8 justify-between w-full p-10 bg-black bg-opacity-75 rounded-lg">
                <div class="flex flex-col gap-4">
                    <h1 class="text-2xl font-bold">Sign up</h1>
                    <small>Start your radio free</small>
                </div>

                <form class="flex flex-col gap-4">
                    <div class="flex flex-col gap-2">
                        <label for="email">Email</label>
                        <InputText id="email" type="email" v-model="value" rounded />
                    </div>

                    <div class="flex justify-end">
                        <Button label="GOOO !" rounded severity="help" @click="$router.push('/create')"/>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import InputText from 'primevue/inputtext';
</script>