<script setup lang="ts">
withDefaults(
  defineProps<{
    coverUrl: string;
    bookTitle: string;
    maxWidthPx?: number;
  }>(),
  {
    maxWidthPx: 140
  }
);
</script>

<template>
  <div
    class="flex h-full w-fit items-center self-center"
    :style="{ maxWidth: `${maxWidthPx}px` }"
    :class="[maxWidthPx]"
  >
    <img class="rounded-lg object-contain" :src="coverUrl" :alt="'Cover of ' + bookTitle" />
  </div>
</template>
