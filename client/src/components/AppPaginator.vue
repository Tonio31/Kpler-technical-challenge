<script setup lang="ts">
import IconChevronLeft from '@/components/icons/IconChevronLeft.vue';
import IconChevronRight from '@/components/icons/IconChevronRight.vue';

const emit = defineEmits<{
  pageChange: [newPageNumber: number];
}>();

const props = defineProps<{
  currentPageNumber: number;
  totalPages: number;
}>();

const previousClicked = () => {
  emit('pageChange', props.currentPageNumber - 1);
};

const nextClicked = () => {
  emit('pageChange', props.currentPageNumber + 1);
};
</script>

<template>
  <div class="flex gap-2 p-4">
    <IconChevronLeft
      class="h-8 w-8 cursor-pointer"
      @click="previousClicked()"
      :class="{ 'pointer-events-none opacity-50': currentPageNumber === 1 }"
    />
    <p class="text-lg font-bold">{{ currentPageNumber }} / {{ totalPages }}</p>
    <IconChevronRight
      class="h-8 w-8 cursor-pointer"
      @click="nextClicked()"
      :class="{ 'pointer-events-none opacity-50': currentPageNumber === totalPages }"
    />
  </div>
</template>
