<script setup lang="ts">
import { computed, type ComputedRef } from 'vue';

const props = withDefaults(
  defineProps<{
    label: string;
    formSubmitted?: boolean;
    required?: boolean;
  }>(),
  {
    formSubmitted: false,
    required: false
  }
);

const model = defineModel({ type: String });

const showInvalidStyle: ComputedRef<boolean> = computed<boolean>(() => {
  return props.required && props.formSubmitted && !model.value;
});
</script>

<template>
  <div class="flex flex-col">
    <label for="appTextarea" class="text-sm" :class="{ 'text-red-600': showInvalidStyle }">
      {{ label }}
    </label>
    <textarea
      class="w-full rounded border-2 border-app-yellow-900 p-1 pr-8"
      :class="{ 'border-red-600': showInvalidStyle }"
      id="appTextarea"
      type="text"
      v-model="model"
    />
    <p class="text-sm text-red-600" v-if="showInvalidStyle">This is a required field</p>
  </div>
</template>
