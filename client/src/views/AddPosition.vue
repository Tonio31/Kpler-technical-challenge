<script setup lang="ts">
import { type Router, useRouter } from 'vue-router';
import AppInput from '@/components/atomic/AppInput.vue';
import { computed, type ComputedRef, type FormHTMLAttributes, ref } from 'vue';
import AppButton from '@/components/atomic/AppButton.vue';
import { ButtonStyle } from '@/models/components';
import { isNumeric } from '@/services/helpers';
import type { Position } from '@/models/vessel';
import { savePosition } from '@/services/api';
import { addPosition } from '@/services/store';

const router: Router = useRouter();

const formRef = ref<FormHTMLAttributes | null>(null);
const isFormSubmitted = ref<boolean>(false);

const isLoading = ref<boolean>(false);
const errorMessage = ref<string>('');

const vesselId = ref<string>('');
const longitude = ref<string>('');
const latitude = ref<string>('');
const createdAt = ref<string>('');

const getErrorMsgForVesselId = (vesselInput: string | undefined): string => {
  if (!vesselInput) {
    return 'Vessel ID is required';
  }

  if (!isNumeric(vesselInput)) {
    return 'Vessel ID should contains only numbers';
  }

  return '';
};

const getErrorMsgForLongitude = (longitude: string | undefined): string => {
  if (!longitude) {
    return 'Longitude is required';
  }

  if (!isNumeric(longitude)) {
    return 'Enter only numbers for longitude';
  }

  const longitudeAsNumber: number = +longitude;
  if (longitudeAsNumber <= -180 || longitudeAsNumber >= 180) {
    return 'Longitude must be a number between -180 & 180';
  }

  return '';
};

const getErrorMsgForLatitude = (latitude: string | undefined): string => {
  if (!latitude) {
    return 'Latitude is required';
  }

  if (!isNumeric(latitude)) {
    return 'Enter only numbers for latitude';
  }

  const latitudeAsNumber: number = +latitude;
  if (latitudeAsNumber <= -90 || latitudeAsNumber >= 90) {
    return 'Latitude must be a number between -90 & 90';
  }

  return '';
};

const getErrorMsgForCreatedAt = (createdAt: string | undefined): string => {
  const regExpDate: RegExp =
    /\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+([+-][0-2]\d:[0-5]\d|Z)/;

  if (createdAt && !regExpDate.test(createdAt)) {
    return 'Wrong format for date, it should be like: "2017-11-10T04:43:07Z"';
  }

  return '';
};

const isFormValid: ComputedRef<boolean> = computed<boolean>((): boolean => {
  return !(
    getErrorMsgForLatitude(latitude.value) ||
    getErrorMsgForLongitude(longitude.value) ||
    getErrorMsgForVesselId(vesselId.value) ||
    getErrorMsgForCreatedAt(createdAt.value)
  );
});

const addPositionFromForm = async (event: Event): Promise<void> => {
  isFormSubmitted.value = true;
  if (isFormValid.value) {
    isLoading.value = true;
    const positionToSave: Position = {
      vesselId: +vesselId.value,
      latitude: +latitude.value,
      longitude: +longitude.value,
      createdAt: new Date().toISOString()
    };
    try {
      const positionAdded: Position = await savePosition(positionToSave);
      addPosition(positionAdded);

      router.push('/');
    } catch (error) {
      if (error instanceof Error) {
        errorMessage.value = error.message;
      } else if (typeof error === 'string') {
        errorMessage.value = `There was an error while saving the position: ${error}`;
      } else {
        errorMessage.value = 'Unknown error';
      }
    }
    isLoading.value = false;
  }
};
</script>

<template>
  <main class="flex h-full flex-col items-center gap-10">
    <h1 class="text-center text-app-yellow-700">Add a single position</h1>
    <form
      class="flex max-w-[700px] flex-col gap-4"
      ref="formRef"
      @submit.prevent="addPositionFromForm"
    >
      <AppInput
        label="Vessel Id"
        v-model="vesselId"
        :validateFn="getErrorMsgForVesselId"
        :formSubmitted="isFormSubmitted"
      ></AppInput>
      <AppInput
        label="Longitude"
        :validateFn="getErrorMsgForLongitude"
        :formSubmitted="isFormSubmitted"
        v-model="longitude"
      ></AppInput>
      <AppInput
        label="Latitude"
        :validateFn="getErrorMsgForLatitude"
        :formSubmitted="isFormSubmitted"
        v-model="latitude"
      ></AppInput>
      <AppInput
        :label="'Date as ISO 8601 - eg:2017-11-10T04:43:07Z (will create record with current date if not provided)'"
        :validateFn="getErrorMsgForCreatedAt"
        :formSubmitted="isFormSubmitted"
        v-model="createdAt"
      ></AppInput>
      <AppButton :style="ButtonStyle.yellowBg" :type="'submit'">Save position</AppButton>
      <p v-if="errorMessage" class="font-bold text-red-600">{{ errorMessage }}</p>
    </form>
  </main>
</template>
