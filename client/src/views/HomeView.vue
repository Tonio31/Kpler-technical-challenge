<script setup lang="ts">
import { ref } from 'vue';
import { api, savePosition, savePositionsInBulk } from '@/services/api';
import AppButton from '@/components/AppButton.vue';
import type { Position } from '@/models/vessel';
import { addPosition, setPositions, vesselStore } from '@/services/store';

const positionJustAdded = ref<Position | null>(null);
const helloWorld = ref<string | null>(null);

const onAddPositionClicked = async () => {
  const positionToAdd: Position = {
    vesselId: 1234,
    createdAt: new Date().toISOString(),
    longitude: 123.83863,
    latitude: 30.49617
  };

  const response: Position = await savePosition(positionToAdd);
  addPosition(response);

  console.log('TONIO  onAddPositionClicked response=', response);

  positionJustAdded.value = response;
};

const onHelloRequested = async () => {
  const response: string = await api<any>('/hello', {
    method: 'POST',
    body: JSON.stringify({ test: 'this is annoying' })
  });

  console.log('TONIO  onHelloRequested response=', response);

  helloWorld.value = response;
};

const addManyPositions = async () => {
  const positionsToAdd: Position[] = [
    {
      vesselId: 4567,
      createdAt: new Date().toISOString(),
      longitude: 120.83863,
      latitude: 38.49617
    },
    {
      vesselId: 4567,
      createdAt: new Date().toISOString(),
      longitude: 126.83863,
      latitude: 39.49617
    }
  ];

  const allPositions: Position[] = await savePositionsInBulk(positionsToAdd);
  setPositions(allPositions);

  console.log('TONIO  onHelloRequested allPositions=', allPositions);
};

console.log('\x1b[44m TONIO ON INIT  \x1b');
</script>

<template>
  <main>
    <h1 class="mb-10 text-center text-app-yellow-700">Vessels positions</h1>

    <div class="flex flex-row items-start gap-10">
      <div>
        <AppButton @click="onAddPositionClicked">Add single position</AppButton>
        <div v-if="positionJustAdded">
          <pre>{{ JSON.stringify(positionJustAdded, null, 2) }}</pre>
        </div>
      </div>

      <div>
        <AppButton @click="onHelloRequested">Hello world</AppButton>
        <div v-if="helloWorld">
          <pre>{{ JSON.stringify(helloWorld, null, 2) }}</pre>
        </div>
      </div>

      <div>
        <AppButton @click="addManyPositions">Add many positions</AppButton>
      </div>
    </div>
    <h1>All positions</h1>
    <pre>{{ JSON.stringify(vesselStore.positions, null, 2) }}</pre>
  </main>
</template>
