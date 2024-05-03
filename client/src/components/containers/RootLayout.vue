<script setup lang="ts">
import { RouterView } from 'vue-router';
import HeaderNavItem from '@/components/atomic/HeaderNavItem.vue';
import { setPositions, vesselStore } from '@/services/store';
import type { Position } from '@/models/vessel';
import { retrieveAllPositions } from '@/services/api';
import { ref } from 'vue';
import AppSpinner from '@/components/atomic/AppSpinner.vue';

const isLoading = ref<boolean>(false);

if (vesselStore.value.positions.length === 0) {
  isLoading.value = true;

  retrieveAllPositions().then((positions: Position[]) => {
    setPositions(positions);
    isLoading.value = false;
  });
}
</script>

<template>
  <div class="mx-auto my-0 flex h-screen max-w-content flex-col gap-4">
    <header class="h-18 flex justify-between gap-4 p-4">
      <RouterLink to="/">
        <img alt="Kpler logo" class="w-40" src="@/assets/kpler_logo.svg" />
      </RouterLink>

      <nav class="flex items-center gap-4">
        <HeaderNavItem :link="'/'">Home</HeaderNavItem>
        <HeaderNavItem :link="'/admin'">Admin</HeaderNavItem>
      </nav>
    </header>
    <div class="grow p-4 shadow-md">
      <div class="flex h-full w-full items-center justify-center" v-if="isLoading">
        <AppSpinner />
      </div>
      <RouterView v-else />
    </div>
  </div>
</template>

<style scoped></style>
