import { describe, expect, it } from 'vitest';

import { mount } from '@vue/test-utils';
import BookComments from '../BookComments.vue';

describe('BookComments', () => {
  it('renders properly', () => {
    const wrapper = mount(BookComments, {
      props: {
        comments: [
          {
            content: 'This book is amazing',
            author: 'Tonio'
          }
        ]
      }
    });
    expect(wrapper.text()).toContain('This book is amazing');
  });

  it('shows an error when the author field is missing', async () => {
    const wrapper = mount(BookComments, {
      props: {
        comments: [
          {
            content: 'This book is amazing',
            author: 'Tonio'
          }
        ]
      }
    });

    const addButton = wrapper.find('button');
    await addButton.trigger('click');

    expect(wrapper.text()).toContain('This is a required field');
  });

  it('adds a new comment', async () => {
    const wrapper = mount(BookComments, {
      props: {
        comments: [
          {
            content: 'This book is amazing',
            author: 'Tonio'
          }
        ]
      }
    });

    const authorInput = wrapper.find('input');
    await authorInput.setValue('Stephane');

    const commentInput = wrapper.find('textarea');
    await commentInput.setValue('I love this book');

    const addButton = wrapper.find('button');
    await addButton.trigger('click');

    expect(wrapper.text()).toContain('I love this book');
  });
});
