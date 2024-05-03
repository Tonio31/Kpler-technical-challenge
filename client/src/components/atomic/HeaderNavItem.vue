<script setup lang="ts">
import { type RouteLocationNormalizedLoaded, useRoute } from 'vue-router';
import { ref, watch } from 'vue';
import AppButton from '@/components/atomic/AppButton.vue';
import { ButtonStyle } from '@/models/components';

defineProps<{
  link: string;
}>();

const currentRouteFullPath = ref<string>('');
const route: RouteLocationNormalizedLoaded = useRoute();

watch(
  () => route.fullPath,
  async () => {
    currentRouteFullPath.value = route.fullPath;
  },
  { immediate: true }
);
</script>

<template>
  <RouterLink :to="link">
    <AppButton
      :style="
        currentRouteFullPath === link ? ButtonStyle.yellowBg : ButtonStyle.transparentBgBlackBorder
      "
    >
      <slot />
    </AppButton>
  </RouterLink>
</template>
