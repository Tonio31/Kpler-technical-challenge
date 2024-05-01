<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Comment } from '@/models/book';
import AppButton from '@/components/AppButton.vue';
import { ButtonStyle } from '@/models/components';
import AppTextarea from '@/components/AppTextarea.vue';
import AppInput from '@/components/AppInput.vue';

const emit = defineEmits<{
  commentAdded: [comment: Comment];
}>();

const props = withDefaults(
  defineProps<{
    comments: Comment[];
  }>(),
  {}
);

const commentsLocal = ref<Comment[]>([]);

watch(
  props.comments,
  () => {
    commentsLocal.value.push(...props.comments);
  },
  { once: true, immediate: true }
);

const newComment = ref<string>('');
const name = ref<string>('');

const formSubmitted = ref<boolean>(false);

const addComment = () => {
  if (newComment.value && name.value) {
    const commentToAdd: Comment = {
      content: newComment.value,
      author: name.value
    };
    commentsLocal.value.push(commentToAdd);
    newComment.value = '';
    name.value = '';
    formSubmitted.value = false;
    emit('commentAdded', commentToAdd);
  } else {
    formSubmitted.value = true;
  }
};
</script>

<template>
  <h3>Comments</h3>
  <template v-if="commentsLocal.length === 0">
    <p>There are no comments for this book, be the first to add a comment below</p>
  </template>
  <template v-else>
    <div v-for="(comment, index) in commentsLocal" :key="comment.content">
      <p>{{ index + 1 }}. {{ comment.content }}</p>
      <p class="text-sm italic">{{ comment.author }}</p>
    </div>
  </template>

  <div class="flex flex-col">
    <AppTextarea
      label="Add new comment:"
      v-model="newComment"
      :required="true"
      :formSubmitted="formSubmitted"
    />
    <AppInput
      label="Your name:"
      v-model="name"
      :formSubmitted="formSubmitted"
      :required="true"
      :showCloseIcon="false"
    />
    <AppButton class="mt-4" :style="ButtonStyle.yellowBg" @click="addComment()">
      Add comment
    </AppButton>
  </div>
</template>

<style scoped></style>
