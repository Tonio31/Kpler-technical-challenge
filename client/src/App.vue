<script setup lang="ts">
import { RouterView } from 'vue-router';
import HeaderNavItem from '@/components/HeaderNavItem.vue';
import type { Position } from '@/models/vessel';
import { getAllPositions } from '@/services/api';
import { setPositions } from '@/services/store';
import AppSpinner from '@/components/AppSpinner.vue';
</script>

<template>
  <div class="mx-auto my-0 flex h-screen max-w-content flex-col gap-4">
    <header class="h-18 flex justify-between gap-4 p-4">
      <RouterLink to="/">
        <img alt="Reedsy logo" class="w-40" src="@/assets/reedsy_logo.png" />
      </RouterLink>

      <nav class="flex items-center gap-4">
        <HeaderNavItem :link="'/'">Home</HeaderNavItem>
      </nav>
    </header>
    <div class="grow shadow-md">
      <Suspense>
        <RouterView />

        <template #fallback>
          <AppSpinner />
        </template>
      </Suspense>
    </div>
  </div>
</template>

<style scoped></style>
