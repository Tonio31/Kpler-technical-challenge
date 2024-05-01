<script setup lang="ts">
import { ButtonStyle } from '@/models/components';

withDefaults(
  defineProps<{
    style?: ButtonStyle;
  }>(),
  {
    style: ButtonStyle.yellowBg
  }
);
</script>

<template>
  <button
    class="w-36 cursor-pointer rounded border-2 px-4 py-2"
    :class="{
      'border-app-yellow-900 bg-white text-app-yellow-900 hover:bg-gray-200':
        style === ButtonStyle.whiteBgYellowBorder,
      'border-app-yellow-700 bg-app-yellow-700 text-black hover:bg-app-yellow-500':
        style === ButtonStyle.yellowBg,
      'border border-black bg-transparent text-black hover:bg-gray-200':
        style === ButtonStyle.transparentBgBlackBorder
    }"
  >
    <slot></slot>
  </button>
</template>
