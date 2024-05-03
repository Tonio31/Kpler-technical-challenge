<script setup lang="ts">
import { vesselStore } from '@/services/store';
import { ButtonStyle } from '@/models/components';
import WorldMap from '@/components/containers/WorldMap.vue';
import AppButton from '@/components/atomic/AppButton.vue';
import { type Router, useRouter } from 'vue-router';

const router: Router = useRouter();

const goToAddPositionView = () => {
  router.push('/add-position');
};
</script>

<template>
  <main class="flex h-full flex-col gap-10">
    <div class="flex justify-between gap-4">
      <h1 class="text-center text-app-yellow-700">Vessels positions</h1>
      <AppButton :style="ButtonStyle.yellowBg" @click="goToAddPositionView">
        Add position
      </AppButton>
    </div>
    <div
      class="flex flex-col items-center justify-center gap-2"
      v-if="vesselStore.positions.length === 0"
    >
      <p class="text-lg font-bold">
        No positions available, head over to the admin to import positions from a CSV file
      </p>
      <RouterLink :to="'/admin'">
        <AppButton :style="ButtonStyle.transparentBgBlackBorder"> Go to Admin page </AppButton>
      </RouterLink>
    </div>
    <div v-else class="flex grow flex-col">
      <WorldMap :positions="vesselStore.positions" />
    </div>
  </main>
</template>
