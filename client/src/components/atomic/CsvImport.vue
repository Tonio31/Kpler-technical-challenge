<script setup lang="ts">
import { ButtonStyle } from '@/models/components';
import AppButton from '@/components/atomic/AppButton.vue';
import Papa from 'papaparse';

import { ref } from 'vue';

const emit = defineEmits<{
  fileParsed: [content: any[]];
}>();

withDefaults(
  defineProps<{
    disabledButton?: boolean;
  }>(),
  {
    disabledButton: false
  }
);

const inputRef = ref<HTMLInputElement | null>(null);

const parseFile = (file: File): void => {
  console.log('TONIO parseFile  file=', file, '   inputRef=', inputRef);
  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    transformHeader: (header: string, index: number): string => {
      return header.trim();
    },
    complete: function (results: any) {
      console.log('TONIO   results=', results);
      emit('fileParsed', results.data);
    }.bind(this)
  });
};

const simulateInputClick = (): void => {
  console.log('TONIO simulateInputClick    inputRef=', inputRef, '   value=', inputRef.value);
  if (inputRef.value) {
    inputRef.value.click();
  }
};

const handleFileUpload = (event: Event) => {
  console.log('TONIO  handleFileUpload event=', event, '   inputRef=', inputRef);
  const target: HTMLInputElement = event.target as HTMLInputElement;
  if (target.files) {
    const file: File = target.files[0];
    parseFile(file);
    target.value = '';
  } else {
    throw new Error(`target.files should always be defined when calling handleFileUpload()`);
  }
};
</script>

<template>
  <div class="relative">
    <AppButton
      :style="ButtonStyle.transparentBgBlackBorder"
      @click="simulateInputClick"
      :disabled="disabledButton"
    >
      Import from CSV
    </AppButton>

    <input
      ref="inputRef"
      id="file"
      type="file"
      accept=".csv"
      @change="handleFileUpload($event)"
      class="absolute -z-10 h-0.5 w-0.5 overflow-hidden opacity-0"
    />
  </div>
</template>
