<script setup lang="ts">
import { ref, watch } from 'vue';
import { setPositions, vesselStore } from '@/services/store';
import type { Position } from '@/models/vessel';
import AppButton from '@/components/AppButton.vue';
import { ButtonStyle } from '@/models/components';
import { deleteAllPositions, savePositionsInBulk } from '@/services/api';
import CsvImport from '@/components/atomic/CsvImport.vue';
import { isNumeric } from '@/services/helpers';
import AppSpinner from '@/components/atomic/AppSpinner.vue';

interface CsvRowVessel {
  latitude: string;
  longitude: string;
  received_time_utc: string;
  vessel_id: string;
}

interface ConvertPositionsReturnValue {
  positions: Position[];
  errors: string[];
}

function isCsvRowVessel(value: any): value is CsvRowVessel {
  return (
    typeof value === 'object' &&
    !Array.isArray(value) &&
    value !== null &&
    typeof value.latitude === 'string' &&
    typeof value.longitude === 'string' &&
    typeof value.received_time_utc === 'string' &&
    typeof value.vessel_id === 'string'
  );
}

const numVessel = ref<number>(0);
const numPositions = ref<number>(0);

const isLoading = ref<boolean>(false);
const errorMessage = ref<string>('');

const errorsParsingCSV = ref<string[]>([]);
const positionsToImport = ref<Position[] | null>(null);

const findVesselNumber = (positions: Position[]): number => {
  const vesselsId: Set<number> = new Set();
  positions.forEach((position: Position): void => {
    vesselsId.add(position.vesselId);
  });

  return Array.from(vesselsId).length;
};

watch(
  vesselStore.value.positions,
  async (newPositions) => {
    numPositions.value = newPositions.length;
    numVessel.value = findVesselNumber(newPositions);

    console.log('TONIO   vesselStore=', vesselStore);
    console.log('\x1b[41m TONIO watch vesselStore  newPositions=', newPositions, '\x1b');
  },
  { immediate: true }
);

const clearAllPositions = async () => {
  errorMessage.value = '';
  console.log('TONIO  clearAllPositions =');
  isLoading.value = true;

  try {
    await deleteAllPositions();
    setPositions([]);
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

const convertCvsDataIntoPositions = (csvRowData: any[]): ConvertPositionsReturnValue => {
  const regExpDate: RegExp = /\d{4}-[01]\d-[0-3]\d\s[0-2]\d:[0-5]\d:[0-5]\d\.\d+/;

  const parsingErrors: string[] = [];
  const positionsFormatted: Position[] = [];

  csvRowData.forEach((row: any, index: number) => {
    if (isCsvRowVessel(row)) {
      const latitudeAsNumber: number = +row.latitude;
      const longitudeAsNumber: number = +row.longitude;
      const vesselIdAsNumber: number = +row.vessel_id;

      const isFormatDateCorrect: boolean = regExpDate.test(row.received_time_utc);

      if (
        isNumeric(latitudeAsNumber) &&
        isNumeric(longitudeAsNumber) &&
        isNumeric(vesselIdAsNumber) &&
        isFormatDateCorrect
      ) {
        positionsFormatted.push({
          createdAt: new Date(row.received_time_utc).toISOString(),
          latitude: latitudeAsNumber,
          longitude: longitudeAsNumber,
          vesselId: vesselIdAsNumber
        });
      } else {
        let errorMessage: string = `Invalid row "${index + 2}": `;
        if (!isNumeric(vesselIdAsNumber)) {
          errorMessage += ` Invalid vessel_id: "${row.vessel_id}".`;
        }
        if (!isNumeric(latitudeAsNumber)) {
          errorMessage += ` Invalid latitude: "${row.latitude}".`;
        }
        if (!isNumeric(longitudeAsNumber)) {
          errorMessage += ` Invalid longitude: "${row.longitude}".`;
        }
        if (!isFormatDateCorrect) {
          errorMessage += ` Invalid date format: "${row.received_time_utc}" (should be like 2017-12-14 00:52:52.000000).`;
        }
        parsingErrors.push(errorMessage);
      }
    } else {
      parsingErrors.push(
        `Unable to parse row ${index + 2}, check that headers are correct. content: ${JSON.stringify(row)}`
      );
    }
  });

  return {
    positions: positionsFormatted,
    errors: parsingErrors
  };
};

const onFileParsed = (content: any[]): void => {
  isLoading.value = true;
  console.log('\x1b[41m TONIO onFileParsed  content=', content, '\x1b');
  setTimeout(() => {
    const results: ConvertPositionsReturnValue = convertCvsDataIntoPositions(content);
    positionsToImport.value = results.positions;
    errorsParsingCSV.value = results.errors;

    console.log('TONIO positionsToImport onFileParsed results=', results);
    isLoading.value = false;
  }, 100);
};

const saveCsvInServer = async (): Promise<void> => {
  console.log('\x1b[41m TONIO saveCsvInServer  positions=', positionsToImport.value, '\x1b');
  if (positionsToImport.value) {
    isLoading.value = true;
    const response: Position[] = await savePositionsInBulk(positionsToImport.value);
    setPositions(response);
    positionsToImport.value = null;
    isLoading.value = false;
  } else {
    console.error(`falsy value for positionsToImport.value:`, positionsToImport.value);
    throw new Error(
      `positionsToImport.value should not be null within saveCsvInServer - investigate bug`
    );
  }
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
      There are currently <span class="font-bold"> {{ numVessel }} vessel</span> and a total of
      <span class="font-bold">{{ numPositions }} positions</span> for all these vessels
    </p>

    <div class="flex items-center gap-4" v-if="numPositions > 0">
      <AppButton
        :style="ButtonStyle.transparentBgRedBorder"
        :disabled="isLoading"
        @click="clearAllPositions"
      >
        Clear all data
      </AppButton>
      <div>
        <p>If you want to start from a clean state, you can delete all records in the database</p>
        <p class="text-red-600">WARNING: you can't revert this action, do it very carefully</p>
      </div>
    </div>

    <div class="flex items-center gap-4">
      <CsvImport @fileParsed="onFileParsed" :disabledButton="isLoading" />
      <div>
        <p>
          You can import positions of vessel using a CSV file, the CSV must have 4 columns in this
          order:
        </p>
        <ul class="list-inside list-disc">
          <li>"vessel_id": number (ex: 5291)</li>
          <li>"received_time_utc": UTC Date with this format: "2017-12-14 00:52:52.000000"</li>
          <li>"latitude": number (ex: 38.40184)</li>
          <li>"vessel_id": number (ex: -79.50869)</li>
        </ul>
      </div>
    </div>

    <div class="flex h-60 items-center justify-center" v-if="isLoading">
      <AppSpinner />
    </div>

    <div
      v-if="positionsToImport"
      class="flex flex-col gap-4"
      :class="{ 'pointer-events-none opacity-50': isLoading }"
    >
      <div v-if="errorsParsingCSV.length > 0" class="border border-red-600 p-2 text-red-600">
        <h4>Errors while parsing the CSV, some rows will be ignored</h4>
        <p v-for="error in errorsParsingCSV">{{ error }}</p>
      </div>
      <h3>Data to import</h3>
      <div class="flex justify-between gap-10">
        <p class="font-bold">Below is an overview of all the data you're going to import</p>
        <AppButton :style="ButtonStyle.yellowBg" @click="saveCsvInServer">Import ALL</AppButton>
      </div>

      <div>
        <div class="grid grid-cols-[1fr_1fr_2fr_1fr_1fr] gap-5 border border-b-0 border-black px-2">
          <p>Index</p>
          <p>Vessel ID</p>
          <p>Date</p>
          <p>latitude</p>
          <p>longitude</p>
        </div>
        <div
          class="grid grid-cols-[1fr_1fr_2fr_1fr_1fr] gap-5 border border-b-0 border-black px-2"
          v-for="(position, index) in positionsToImport"
          :key="index"
          :class="{ 'bg-blue-100': index % 2 === 0, 'bg-yellow-100': index % 2 === 1 }"
        >
          <p>{{ index }}</p>
          <p>{{ position.vesselId }}</p>
          <p>{{ position.createdAt }}</p>
          <p>{{ position.latitude }}</p>
          <p>{{ position.longitude }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
