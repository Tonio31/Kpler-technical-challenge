<script setup lang="ts">
import { ref, watch } from 'vue';
import { vesselStore } from '@/services/store';
import type { Position } from '@/models/vessel';
import AppButton from '@/components/AppButton.vue';
import { ButtonStyle } from '@/models/components';
import AppSpinner from '@/components/atomic/AppSpinner.vue';
import { deleteAllPositions } from '@/services/api';

const numVessel = ref<number>(0);
const numPositions = ref<number>(0);

const isLoading = ref<boolean>(false);
const errorMessage = ref<string>('');

const findVesselNumber = (positions: Position[]): number => {
  const vesselsId: Set<number> = new Set();
  positions.forEach((position: Position): void => {
    vesselsId.add(position.vesselId);
  });

  return Array.from(vesselsId).length;
};

watch(
  vesselStore,
  async (newVesselStore, oldQuestion) => {
    numPositions.value = newVesselStore.positions.length;
    numVessel.value = findVesselNumber(newVesselStore.positions);

    console.log('TONIO   vesselStore=', vesselStore);
    console.log('\x1b[41m TONIO watch vesselStore  newVesselStore=', newVesselStore, '\x1b');
  },
  { immediate: true }
);

const clearAllPositions = async () => {
  errorMessage.value = '';
  console.log('TONIO  clearAllPositions =');
  isLoading.value = true;

  try {
    await deleteAllPositions();
  } catch (error) {
    console.error(`Error during delete: e=`, error);
    if (error instanceof Error) {
      errorMessage.value = error.message;
    } else if (typeof error === 'string') {
      errorMessage.value = error;
    } else {
      errorMessage.value = 'Unknown error';
    }
  }
  isLoading.value = false;
};
</script>

<template>
  <div class="flex flex-col gap-10">
    <h1>Admin Section - Danger Zone</h1>
    <p class="font-bold">
      In a real application, this will be protected by username / password and only users with
      special privileges would be able to access this
    </p>

    <p>
      There are currently {{ numVessel }} vessel and a total of {{ numPositions }} positions for all
      these vessels
    </p>
    <div class="flex justify-center gap-4">
      <AppSpinner v-if="isLoading" />
      <template v-else>
        <AppButton :style="ButtonStyle.transparentBgBlackBorder" @click="clearAllPositions">
          Import from CSV
        </AppButton>

        <AppButton
          :style="ButtonStyle.transparentBgRedBorder"
          :disabled="numPositions === 0"
          @click="clearAllPositions"
        >
          Clear all data
        </AppButton>
      </template>
    </div>
    <p v-if="errorMessage" class="text-center text-lg font-bold text-red-600">
      {{ errorMessage }}
    </p>
  </div>
</template>

<style scoped></style>
