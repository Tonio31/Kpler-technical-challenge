<script setup lang="ts">
import { onMounted, ref } from 'vue';
import IconClose from '@/components/icons/IconClose.vue';
import { VESSEL_ID_QUERY_PARAM_KEY, type VesselPath } from '@/models/vessel';
import { type LocationQueryValue, type RouteLocationNormalizedLoaded, useRoute } from 'vue-router';

const emit = defineEmits<{
  vesselSelectionChanged: [allVesselSelected: string[]];
}>();

withDefaults(
  defineProps<{
    vesselsPath: VesselPath[];
    vesselIdToPreSelect: string[];
  }>(),
  {
    vesselsPath: () => []
  }
);

const route: RouteLocationNormalizedLoaded = useRoute();

const vesselsIdSelected = ref<string[]>([]);

const onVesselClick = (vesselId: string): void => {
  if (vesselsIdSelected.value.includes(vesselId)) {
    const indexToRemove: number = vesselsIdSelected.value.indexOf(vesselId);
    vesselsIdSelected.value.splice(indexToRemove, 1);
  } else {
    vesselsIdSelected.value.push(vesselId);
  }
  emit(`vesselSelectionChanged`, vesselsIdSelected.value);
};

onMounted(() => {
  const vesselIdsInUrl: LocationQueryValue | LocationQueryValue[] | null =
    route.query[VESSEL_ID_QUERY_PARAM_KEY];
  console.log('TONIO  onMounted vesselIdsInUrl=', vesselIdsInUrl);
  if (vesselIdsInUrl && typeof vesselIdsInUrl === 'string') {
    console.log('TONIO  onMounted IT IS A STRING vesselIdsInUrl=', vesselIdsInUrl);
    vesselsIdSelected.value = vesselIdsInUrl.split(',');
    emit(`vesselSelectionChanged`, vesselsIdSelected.value);
  }
});
</script>

<template>
  <div class="flex flex-wrap items-center gap-4">
    <p>Filter by Vessel ID:</p>

    <div
      v-for="vessel in vesselsPath"
      :key="vessel.vesselId"
      :class="[vesselsIdSelected.includes(vessel.vesselId) ? '' : '']"
      :style="[
        vesselsIdSelected.includes(vessel.vesselId)
          ? {
              backgroundColor: vessel.strokeColor
            }
          : {
              backgroundColor: 'white',
              color: vessel.strokeColor
            },
        {
          borderColor: vessel.strokeColor
        }
      ]"
      class="relative cursor-pointer rounded border-4 py-1 pl-2 pr-10 text-black hover:opacity-80"
      @click="() => onVesselClick(vessel.vesselId)"
    >
      <span class="font-bold">{{ vessel.vesselId }}</span>
      <div
        class="icon-filter-selected absolute bottom-0 right-2 top-0 z-10 my-auto py-1 text-black"
        v-if="vesselsIdSelected.includes(vessel.vesselId)"
      >
        <IconClose class="h-full w-full" />
      </div>
    </div>
  </div>
</template>
