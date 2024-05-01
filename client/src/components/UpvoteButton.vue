<script setup lang="ts">
import { ref } from 'vue';
import { ButtonStyle } from '@/models/components';
import AppButton from '@/components/AppButton.vue';

const props = defineProps<{
  upvoted: boolean;
}>();

const upVotedLocal = ref<boolean>(props.upvoted);

const toggleUpVoted = () => {
  upVotedLocal.value = !upVotedLocal.value;
};
</script>

<template>
  <AppButton
    :style="upVotedLocal ? ButtonStyle.whiteBgYellowBorder : ButtonStyle.yellowBg"
    @click="toggleUpVoted()"
  >
    {{ upVotedLocal ? 'Upvoted' : 'Upvote' }}
  </AppButton>
</template>
