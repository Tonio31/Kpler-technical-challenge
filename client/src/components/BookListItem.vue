<script setup lang="ts">
import type { Book } from '@/models/book';
import { computed, type ComputedRef } from 'vue';
import BookCover from '@/components/BookCover.vue';
import UpvoteButton from '@/components/UpvoteButton.vue';
import { type Router, useRouter } from 'vue-router';
import UpvotedSummary from '@/components/UpvotedSummary.vue';

const MAX_LENGTH_SYNOPSIS: number = 200;

const router: Router = useRouter();

const props = defineProps<{
  book: Book;
  bookNumber: number | undefined;
}>();

const synopsisTruncated: ComputedRef<string> = computed<string>(() => {
  return props.book.synopsis.length > MAX_LENGTH_SYNOPSIS
    ? `${props.book.synopsis.slice(0, MAX_LENGTH_SYNOPSIS - 3)}...`
    : props.book.synopsis;
});

const goToBookDetailsPage = () => {
  router.push(`/book/${props.book.slug}`);
};
</script>

<template>
  <div class="flex justify-between gap-4">
    <div class="flex flex-col gap-2">
      <div class="flex items-end gap-2">
        <h2 class="cursor-pointer text-app-yellow-900" @click="goToBookDetailsPage()">
          <template v-if="bookNumber !== undefined">{{ bookNumber }}. </template>{{ book.title }}
        </h2>
        <p class="text-sm leading-7">({{ book.rating }}/10)</p>
      </div>
      <p class="text-sm italic">{{ book.author }}</p>
      <BookCover
        class="cursor-pointer md:hidden"
        :coverUrl="book.cover"
        :bookTitle="book.title"
        @click="goToBookDetailsPage()"
      />
      <div class="grow">
        <p>{{ synopsisTruncated }}</p>
      </div>

      <div class="flex items-center gap-4">
        <UpvoteButton :upvoted="book.upvoted" />
        <UpvotedSummary :votes="book.upvotes" />
      </div>
    </div>

    <BookCover
      class="hidden cursor-pointer md:block"
      :coverUrl="book.cover"
      :bookTitle="book.title"
      @click="goToBookDetailsPage()"
    />
  </div>
</template>

<style scoped></style>
