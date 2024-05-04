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
  vesselStore.value.positions.splice(0);
  vesselStore.value.positions.push(...positions);
  return vesselStore;
};
