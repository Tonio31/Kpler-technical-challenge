<script setup lang="ts">
import IconClose from '@/components/icons/IconClose.vue';
import { computed, type ComputedRef } from 'vue';

const props = withDefaults(
  defineProps<{
    label: string;
    formSubmitted?: boolean;
    required?: boolean;
    showCloseIcon?: boolean;
  }>(),
  {
    formSubmitted: false,
    required: false,
    showCloseIcon: true
  }
);

const model = defineModel({ type: String });

const clearInput = () => {
  model.value = '';
};

const showInvalidStyle: ComputedRef<boolean> = computed<boolean>(() => {
  return props.required && props.formSubmitted && !model.value;
});
</script>

<template>
  <div class="flex flex-col">
    <label for="appInput" class="text-sm" :class="{ 'text-red-600': showInvalidStyle }">
      {{ label }}
    </label>
    <div class="relative w-full">
      <input
        class="w-full rounded border-2 border-app-yellow-900 p-1 pr-8"
        :class="{ 'border-red-600': showInvalidStyle }"
        id="appInput"
        type="text"
        v-model="model"
      />
      <IconClose
        v-if="showCloseIcon"
        class="absolute right-1 top-0 h-full cursor-pointer"
        @click="clearInput()"
      />
    </div>
    <p class="text-sm text-red-600" v-if="showInvalidStyle">This is a required field</p>
  </div>
</template>
