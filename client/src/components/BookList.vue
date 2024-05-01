<script setup lang="ts">
import type { BookFrontEnd } from '@/models/book';
import BookListItem from '@/components/BookListItem.vue';
import { computed, type ComputedRef, ref, watch } from 'vue';
import AppInput from '@/components/AppInput.vue';
import AppPaginator from '@/components/AppPaginator.vue';

const props = defineProps<{
  books: BookFrontEnd[];
}>();

const NUMBER_BOOK_PER_PAGE: number = 4;

const searchText = ref<string>('');
const pageNumber = ref<number>(1);

const booksFiltered: ComputedRef<BookFrontEnd[]> = computed<BookFrontEnd[]>(() => {
  const searchTextLowercase: string = searchText.value.toLowerCase();
  return props.books.filter((book: BookFrontEnd) => {
    return (
      book.title.toLowerCase().includes(searchTextLowercase) ||
      book.synopsis.toLowerCase().includes(searchTextLowercase)
    );
  });
});

const booksDisplayedOnCurrentPage: ComputedRef<BookFrontEnd[]> = computed<BookFrontEnd[]>(() => {
  return booksFiltered.value.slice(
    (pageNumber.value - 1) * NUMBER_BOOK_PER_PAGE,
    pageNumber.value * NUMBER_BOOK_PER_PAGE
  );
});

const totalPages: ComputedRef<number> = computed<number>(() => {
  const totalNumberBooks: number = booksFiltered.value.length;
  return Math.ceil(totalNumberBooks / NUMBER_BOOK_PER_PAGE);
});

const onPageChange = (newPageNumber: number): void => {
  pageNumber.value = newPageNumber;
};

watch(
  searchText,
  () => {
    pageNumber.value = 1;
  },
  { immediate: false }
);
</script>

<template>
  <div class="flex flex-col gap-2">
    <AppInput class="p-4" :label="'Search books'" v-model="searchText" />
    <div
      v-if="booksDisplayedOnCurrentPage.length === 0"
      class="w-full p-4 text-center text-lg font-bold"
    >
      We don't have any books matching your search.
    </div>

    <template v-else>
      <div v-for="(book, index) in booksDisplayedOnCurrentPage" :key="book.title">
        <BookListItem
          :book="book"
          :bookNumber="book.ranking"
          class="p-4"
          :class="{ 'bg-white': index % 2 === 0 }"
        />
      </div>
      <div class="flex w-full items-center justify-center">
        <AppPaginator
          :currentPageNumber="pageNumber"
          :totalPages="totalPages"
          @pageChange="onPageChange"
        />
      </div>
    </template>
  </div>
</template>
