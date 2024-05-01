<script setup lang="ts">
import { ref } from 'vue';
import type { Book, BookFrontEnd, Comment } from '@/models/book';
import { type RouteLocationNormalizedLoaded, useRoute } from 'vue-router';
import UpvotedSummary from '@/components/UpvotedSummary.vue';
import UpvoteButton from '@/components/UpvoteButton.vue';
import BookCover from '@/components/BookCover.vue';
import BookComments from '@/components/BookComments.vue';
import AppSpinner from '@/components/AppSpinner.vue';

const book = ref<BookFrontEnd | null>(null);

async function getBook(): Promise<Book> {
  const route: RouteLocationNormalizedLoaded = useRoute();
  const response = await fetch(`http://localhost:3000/books/${route.params.id}`, {
    method: 'GET'
  });
  return response.json();
}

getBook().then((data: Book) => {
  book.value = {
    ...data,

    // This is MOCK DATA is order to test comments, it will usually come form the back end
    comments: [
      {
        content: 'This book is amazing',
        author: 'Tonio'
      }
    ]
  };
});

const saveBookWithNewComment: (newComment: Comment) => void = (newComment: Comment): void => {
  if (book.value) {
    if (book.value.comments) {
      book.value.comments.push(newComment);
    } else {
      book.value.comments = [newComment];
    }
  }

  // TODO Save comment in the back end
};
</script>

<template>
  <div v-if="!book" class="flex h-full w-full items-center justify-center">
    <AppSpinner />
  </div>
  <div v-else class="flex h-full flex-col gap-10 bg-white p-8">
    <div class="flex flex-col items-center justify-between gap-4 sm:flex-row">
      <div class="w-full sm:w-auto">
        <h2 class="text-app-yellow-900">
          {{ book.title }}
        </h2>
        <p class="text-sm italic">{{ book.author }}</p>
      </div>
      <div class="flex w-full items-center gap-4 sm:w-auto">
        <UpvotedSummary :votes="book.upvotes" />
        <UpvoteButton :upvoted="book.upvoted" />
      </div>
    </div>
    <BookCover class="" :coverUrl="book.cover" :bookTitle="book.title" :maxWidthPx="500" />

    <div>
      <h4>Synopsis</h4>
      <p>{{ book.synopsis }}</p>
    </div>
    <p class="text-sm font-bold">Rating: {{ book.rating }}/10</p>

    <div class="w-full border-t-2 border-black"></div>

    <BookComments :comments="book.comments || []" @commentAdded="saveBookWithNewComment" />
  </div>
</template>

<style scoped></style>
