<script setup lang="ts">
import { ButtonStyle } from '@/models/components';

withDefaults(
  defineProps<{
    disabled?: boolean;
    type?: 'submit' | 'reset' | 'button' | undefined;
    style?: ButtonStyle;
  }>(),
  {
    disabled: false,
    type: 'button',
    style: ButtonStyle.yellowBg
  }
);
</script>

<template>
  <button
    class="w-36 cursor-pointer rounded border-2 px-4 py-2"
    :type="type"
    :class="{
      'border-app-yellow-900 bg-white text-app-yellow-900 hover:bg-gray-200':
        style === ButtonStyle.whiteBgYellowBorder,
      'border-app-yellow-700 bg-app-yellow-700 text-black hover:bg-app-yellow-500':
        style === ButtonStyle.yellowBg,
      'border border-black bg-transparent text-black hover:bg-gray-200':
        style === ButtonStyle.transparentBgBlackBorder,
      'border border-red-600 bg-transparent font-bold text-red-600 hover:bg-red-200':
        style === ButtonStyle.transparentBgRedBorder,
      'pointer-events-none opacity-50': disabled
    }"
  >
    <slot></slot>
  </button>
</template>
