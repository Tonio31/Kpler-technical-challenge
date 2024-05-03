import { ref } from 'vue';
import type { Position } from '@/models/vessel';
import type { Ref } from '@vue/reactivity';

export interface VesselStore {
  positions: Position[];
}

export const vesselStore: Ref<VesselStore> = ref<VesselStore>({
  positions: []
});

export const addPosition = (position: Position): Ref<VesselStore> => {
  vesselStore.value.positions.push(position);
  return vesselStore;
};

export const setPositions = (positions: Position[]): Ref<VesselStore> => {
  console.log(
    'TONIO 0 setPositions positions=',
    positions,
    '   vesselStore.value.positions=',
    vesselStore.value.positions
  );
  vesselStore.value.positions.splice(0);
  vesselStore.value.positions.push(...positions);
  console.log('TONIO 10 setPositions  vesselStore.value.positions=', vesselStore.value.positions);
  return vesselStore;
};
