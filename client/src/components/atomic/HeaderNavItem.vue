<script setup lang="ts">
import AppButton from '@/components/atomic/AppButton.vue';
import { ButtonStyle } from '@/models/components';

defineProps<{
  link: string;
}>();
</script>

<template>
  <RouterLink :to="link">
    <AppButton :style="ButtonStyle.transparentBgBlackBorder">
      <slot />
    </AppButton>
  </RouterLink>
</template>
