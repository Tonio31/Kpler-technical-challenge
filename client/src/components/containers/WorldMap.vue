<script setup lang="ts">
import { GoogleMap, Polyline } from 'vue3-google-map';
import type {
  LatLng,
  Position,
  PositionAndTimeFilter,
  TimeFilter,
  VesselPath
} from '@/models/vessel';
import { ref, watch } from 'vue';
import AppSpinner from '@/components/atomic/AppSpinner.vue';
import MapVesselFilter from '@/components/containers/MapVesselFilter.vue';
import { type Router, useRouter } from 'vue-router';
import { ButtonStyle } from '@/models/components';
import AppButton from '@/components/atomic/AppButton.vue';
import { onUnmounted } from '@vue/runtime-core';
import {
  computePositionsPerVesselAndTimeFilters,
  computeVesselPath,
  filterVesselPath
} from '@/services/vesselsHelper';
import IconPlay from '@/components/icons/IconPlay.vue';
import IconPause from '@/components/icons/IconPause.vue';

const props = defineProps<{
  positions: Position[];
}>();

const router: Router = useRouter();

const mapRef = ref<InstanceType<typeof GoogleMap> | null>(null);

const apiKey = ref<string>(import.meta.env.VITE_GOOGLE_API_KEY);
const center = ref<LatLng>({ lat: 0, lng: 0 });
const isLoading = ref<boolean>(false);
const allVesselPaths = ref<VesselPath[]>([]);
const vesselPathsFiltered = ref<VesselPath[]>([]);
const timeFilter = ref<TimeFilter | null>(null);
const allPossibleTimeFilters = ref<TimeFilter[]>([]);
const historyTimeoutIds = ref<ReturnType<typeof setTimeout>[]>([]);

const vesselIdSelected = ref<string[]>([]);

const clearAllHistoryTimeout = () => {
  historyTimeoutIds.value.forEach((timeoutId: ReturnType<typeof setTimeout>) => {
    clearTimeout(timeoutId);
  });
  historyTimeoutIds.value = [];
};

const playPauseHistory = () => {
  if (historyTimeoutIds.value.length > 0) {
    clearAllHistoryTimeout();
  } else {
    allPossibleTimeFilters.value.forEach((time: TimeFilter, index: number) => {
      historyTimeoutIds.value.push(
        setTimeout(() => {
          timeFilter.value = time;

          if (index === allPossibleTimeFilters.value.length - 1) {
            clearAllHistoryTimeout();
          }
        }, index * 300)
      );
    });
  }
};

const onVesselIdChange = (vesselsIdSelected: string[]): void => {
  vesselIdSelected.value = [...vesselsIdSelected];
  router.push({ query: { vesselIds: vesselsIdSelected.join(',') } });
};

watch(
  [() => props.positions, () => mapRef.value?.ready],
  ([newPositions, isGoogleMapReady]) => {
    isLoading.value = true;
    if (newPositions && newPositions.length > 0 && isGoogleMapReady) {
      setTimeout(async () => {
        const { timeFilters, positionsPerVessel }: PositionAndTimeFilter =
          computePositionsPerVesselAndTimeFilters(newPositions);
        allPossibleTimeFilters.value = timeFilters;

        allVesselPaths.value = computeVesselPath(positionsPerVessel);
        isLoading.value = false;
      }, 100);
    }
  },
  { immediate: true }
);

watch(
  [() => allVesselPaths.value, () => vesselIdSelected.value, () => timeFilter.value],
  async ([newVesselPaths, newVesselIdSelected, newTimeFilter]) => {
    vesselPathsFiltered.value = filterVesselPath(
      newVesselPaths,
      newVesselIdSelected,
      newTimeFilter
    );
  },
  { immediate: true }
);

onUnmounted(() => {
  clearAllHistoryTimeout();
});
</script>

<template>
  <div class="col relative flex grow flex-col gap-4">
    <div v-if="isLoading" class="flex h-full w-full items-center justify-center">
      <AppSpinner />
    </div>

    <div :class="{ 'h-0 w-0 opacity-0': isLoading }" class="flex flex-col gap-4">
      <div class="flex flex-col justify-between gap-4 md:flex-row">
        <MapVesselFilter
          :vesselsPath="allVesselPaths"
          :vesselIdToPreSelect="vesselIdSelected"
          @vesselSelectionChanged="onVesselIdChange"
        />
        <AppButton :style="ButtonStyle.yellowBg" @click="playPauseHistory">
          <IconPlay class="h-10 w-full" v-if="historyTimeoutIds.length === 0" />
          <IconPause class="h-10 w-full" v-if="historyTimeoutIds.length > 0" />
        </AppButton>
      </div>
      <GoogleMap
        ref="mapRef"
        :apiKey="apiKey"
        style="width: 100%; height: 500px"
        :center="center"
        :zoom="2"
      >
        <Polyline v-for="path in vesselPathsFiltered" :options="path" />
      </GoogleMap>
    </div>
  </div>
</template>

<style scoped></style>
