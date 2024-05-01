<script setup lang="ts">
defineProps<{
  votes: number;
}>();
</script>

<template>
  <p>Upvoted {{ votes }} {{ votes === 1 ? 'time' : 'times' }}</p>
</template>
