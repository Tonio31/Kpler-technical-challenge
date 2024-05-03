<script setup lang="ts">
import { GoogleMap, Polyline } from 'vue3-google-map';
import type { LatLng, Position, PositionsPerVessel, VesselPath } from '@/models/vessel';
import { ref, watch } from 'vue';
import { getHtmlColorCodeForNumber, sortPositionsByTimestamp } from '@/services/helpers';
import AppSpinner from '@/components/atomic/AppSpinner.vue';
import MapVesselFilter from '@/components/containers/MapVesselFilter.vue';
import { type Router, useRouter } from 'vue-router';

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

const vesselIdSelected = ref<string[]>([]);

const getPositionsPerVessel = (positions: Position[]): PositionsPerVessel => {
  const positionsPerVessel: PositionsPerVessel = {};

  const allPositionsSorted: Position[] = sortPositionsByTimestamp(positions);

  console.log('TONIO  computePositions allPositionsSorted=', allPositionsSorted);
  allPositionsSorted.forEach((position: Position) => {
    if (!positionsPerVessel[position.vesselId]) {
      positionsPerVessel[position.vesselId] = [];
    }

    positionsPerVessel[position.vesselId].push(position);
  });

  console.log('TONIO  computePositions positionsPerVessel=', positionsPerVessel);

  return positionsPerVessel;
};

const computeVesselPath = (vesselsPositions: PositionsPerVessel): VesselPath[] => {
  const lineSymbol = {
    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
  };

  const vesselPaths: VesselPath[] = [];
  let index: number = 0;
  Object.entries(vesselsPositions).forEach(([vesselId, positions]: [string, Position[]]) => {
    const randomColor: string = getHtmlColorCodeForNumber(index);
    vesselPaths.push({
      vesselId,
      path: positions.map((position: Position): LatLng => {
        return {
          lat: position.latitude,
          lng: position.longitude
        };
      }),
      icons: [
        {
          icon: lineSymbol,
          offset: '100%'
        }
      ],
      geodesic: true,
      strokeColor: randomColor,
      strokeOpacity: 1.0,
      strokeWeight: 2
    });

    index += 1;
  });

  return vesselPaths;
};

const filterVesselPath = (
  vesselPathToFilter: VesselPath[],
  vesselIdToInclude: string[]
): VesselPath[] => {
  console.log(
    '\x1b[41m TONIO  filterVesselPath vesselPathToFilter=',
    vesselPathToFilter,
    '  vesselIdToInclude=',
    vesselIdToInclude,
    '\x1b'
  );
  return vesselPathToFilter.filter((vesselPath: VesselPath): boolean => {
    if (vesselIdToInclude.length === 0) {
      return true;
    } else if (vesselIdToInclude.includes(vesselPath.vesselId)) {
      return true;
    }

    return false;
  });
};

const onPolylineClick = (event: any, path: VesselPath): void => {
  console.log('TONIO onPolylineClick  event=', event, '   path=', path);
};

const onVesselIdChange = (vesselsIdSelected: string[]): void => {
  console.log('TONIO onVesselIdChange  vesselsIdSelected=', vesselsIdSelected);
  vesselIdSelected.value = [...vesselsIdSelected];
  router.push({ query: { vesselIds: vesselsIdSelected.join(',') } });
};

watch(
  [() => props.positions, () => mapRef.value?.ready],
  ([newPositions, isGoogleMapReady]) => {
    console.log(
      'TONIO   newVesselIdSelected=',
      '  newPositions=',
      newPositions,
      ' isGoogleMapReady=',
      isGoogleMapReady
    );
    isLoading.value = true;
    if (newPositions && newPositions.length > 0 && isGoogleMapReady) {
      setTimeout(async () => {
        const positionsPerVessel: PositionsPerVessel = getPositionsPerVessel(newPositions);

        allVesselPaths.value = computeVesselPath(positionsPerVessel);
        isLoading.value = false;
      }, 100);
      console.log('TONIO   WATCH newPositions=', newPositions);
    }
  },
  { immediate: true }
);

watch(
  [() => allVesselPaths.value, () => vesselIdSelected.value],
  async ([newVesselPaths, newVesselIdSelected]) => {
    console.log(
      'TONIO   newVesselIdSelected=',
      newVesselIdSelected,
      '  newVesselPaths=',
      newVesselPaths
    );
    //TODO TONIO BUG WHEN LOADING SCREEN newVesselIdSelected=['']
    vesselPathsFiltered.value = filterVesselPath(newVesselPaths, newVesselIdSelected);

    console.log('TONIO   WATCH vesselPathsFiltered.value=', vesselPathsFiltered.value);
  },
  { immediate: true }
);
</script>

<template>
  <div class="col relative flex grow flex-col gap-4">
    <div v-if="isLoading" class="flex h-full w-full items-center justify-center">
      <AppSpinner />
    </div>

    <div :class="{ 'h-0 w-0 opacity-0': isLoading }" class="flex flex-col gap-4">
      <MapVesselFilter
        :vesselsPath="allVesselPaths"
        :vesselIdToPreSelect="vesselIdSelected"
        @vesselSelectionChanged="onVesselIdChange"
      />
      <GoogleMap
        ref="mapRef"
        :apiKey="apiKey"
        style="width: 100%; height: 500px"
        :center="center"
        :zoom="2"
      >
        <Polyline
          v-for="path in vesselPathsFiltered"
          :options="path"
          @click="(event) => onPolylineClick(event, path)"
        />
      </GoogleMap>
    </div>
  </div>
</template>

<style scoped></style>
