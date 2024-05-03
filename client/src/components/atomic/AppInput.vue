<script setup lang="ts">
import IconClose from '@/components/icons/IconClose.vue';
import { computed, type ComputedRef } from 'vue';

const props = withDefaults(
  defineProps<{
    label: string;
    formSubmitted?: boolean;
    showCloseIcon?: boolean;
    validateFn?: (value: string | undefined) => string;
  }>(),
  {
    formSubmitted: false,
    required: false,
    showCloseIcon: false
  }
);

const model = defineModel({ type: String });

const clearInput = () => {
  model.value = '';
};

const errorMessage: ComputedRef<string> = computed<string>((): string => {
  if (typeof props.validateFn === 'function') {
    const errorFromValidateFn: string = props.validateFn(model.value);
    return props.formSubmitted ? errorFromValidateFn : '';
  }

  return '';
});
</script>

<template>
  <div class="flex flex-col">
    <label for="appInput" class="text-sm" :class="{ 'text-red-600': errorMessage }">
      {{ label }}
    </label>
    <div class="relative w-full">
      <input
        class="w-full rounded border-2 border-app-yellow-900 p-1 pr-8"
        :class="{ 'border-red-600 text-red-600': errorMessage }"
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
    <p class="text-sm text-red-600" v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>
