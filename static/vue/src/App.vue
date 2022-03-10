<script setup>
import { ref, unref, watch } from 'vue'

const showModal = ref(false)
const formDesciption = ref(null)
const formAttachments = ref([])
const attachmentInput = ref(null)
const invalidDesciption = ref(false)

const assignAttachment = () => {
  const file = unref(attachmentInput).files[0]
  // console.log(file)
  formAttachments.value = [...formAttachments.value, { file, key: Date.now(), src: URL.createObjectURL(file) }]
  unref(attachmentInput).value = null
  // attachmentSrc.value = URL.createObjectURL(formAttachment.value)
  // console.log(unref(attachmentInput).files)
}

const removeAttachment = idx => {
  formAttachments.value = unref(formAttachments).filter((_, i) => i !== idx)
}

const clearForm = () => {
  formDesciption.value = null
  formAttachments.value = []
}

watch(showModal, clearForm)

watch(formDesciption, () => {
  if (unref(invalidDesciption)) invalidDesciption.value = false
})

const handleSubmit = async () => {
  if (!unref(formDesciption)) {
    invalidDesciption.value = true
  } else {
    const formData = new FormData()
    formData.append('description', unref(formDesciption))
    unref(formAttachments).forEach(({ file }) => {
      formData.append('attachments', file)
    })

    const res = await fetch(
      '/api/todos',
      {
        method: 'POST',
        body: formData
      }
    )
    const { data } = await res.json()
    showModal.value = false
    console.log(data)
  }
}
</script>

<template>
  <header class="todo-header">
    <h1>
      {{ 'Noop Blueprint' }}
      <span>{{ 'Todo App' }}</span>
    </h1>
  </header>
  <template v-if="false">
    <hr class="divider">
    <section class="todo-list">
      <!-- Foo -->
    </section>
  </template>
  <hr class="divider">
  <section class="todo-create">
    <div>
      <button @click="showModal = true">
        {{ 'New Todo' }}
      </button>
    </div>
  </section>
  <section
    v-if="showModal"
    class="todo-modal"
    @click="showModal = false"
  >
    <form
      class="todo-form"
      @submit.prevent="handleSubmit"
      @click.stop
    >
      <div class="todo-form-row">
        <h5 class="todo-form-header">
          <button
            class="todo-close"
            title="Close modal"
            type="button"
            @click="showModal = false"
          >
            {{ '×' }}
          </button>
          <span>{{ 'Provide Todo Details…' }}</span>
        </h5>
      </div>
      <hr class="divider">
      <div class="todo-form-row">
        <label for="form-description">Description (required)</label>
        <input
          id="form-description"
          v-model="formDesciption"
          type="text"
          autocomplete="off"
          placeholder="What needs to be done?"
        >
        <label v-if="invalidDesciption" class="form-error">Todo description is required</label>
      </div>
      <div class="todo-form-row">
        <label for="form-attachment">Attachments (optional, PNG or JPG)</label>
        <input
          id="form-attachment"
          ref="attachmentInput"
          type="file"
          accept=".jpg, .jpeg, .png"
          @input="assignAttachment"
        >
        <div class="form-preview-grid">
          <span v-for="({ src, key }, idx) in formAttachments" :key="key" class="form-preview-image">
            <img :src="src">
            <button type="button" class="form-preview-remove" title="Remove Attachment" @click.prevent="removeAttachment(idx)">
              <span>
                {{ '×' }}
              </span>
            </button>
          </span>
        </div>
      </div>
      <hr class="divider">
      <div class="todo-form-row">
        <input
          id="form-submit"
          type="submit"
          value="Create Todo"
        >
      </div>
    </form>
  </section>
</template>

<style>
@import './reboot.css';

:root {
  --noop-primary-color: #0091ff;
  --noop-bg-color: #f4f3ef;
}

#app {
  min-height: 100vh;
  background-color: var(--noop-bg-color);
}

.divider {
  margin: 0 auto;
  flex-shrink: 0;
}

.todo-header, .todo-list, .todo-create {
  padding: 1rem;
  max-width: 640px;
  margin: auto;
}

.todo-create div {
  width: min(640, calc(100vw - 2rem));
  text-align: center;
}

.todo-create div button {
  color: #fff;
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
  background-color: var(--noop-primary-color);
  border: var(--noop-primary-color) solid;
}

.todo-header h1 {
  text-align: center;
  color: var(--noop-primary-color);
  margin-bottom: 0;
  font-weight: 300;
  filter: brightness(80%);
}

.todo-header h1 span {
  /* font-size: 0.75em; */
  font-family: 'Brush Script MT', cursive;
  /* letter-spacing: 1px; */
}

.todo-modal {
  position: absolute;
  padding: 1rem;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgb(0 0 0 / 50%);
  display: flex;
  overflow-x: hidden;
  flex-direction: column;
  align-items: center;
}

.todo-form {
  padding: 1rem;
  background-color: #fff;
  border: var(--bs-gray-400) solid 1px;
  border-radius: 0.25rem;
  margin: auto;
  width: min(480px, calc(100vw - 2rem));
  max-height: calc(100vh - 2rem);
  overflow-y: scroll;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.todo-form .divider {
  margin: 0 -1rem;
}

.todo-form-header {
  margin: 0;
}

.todo-close {
  float: right;
  font-size: 1.25rem;
  color: var(--bs-secondary);
  display: flex;
  align-items: center;
  padding: 0 0.5rem;
  margin-top: -0.5rem;
  margin-right: -0.5rem;
  cursor: pointer;
  border: none;
  background: none;
}

.todo-form-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

#form-description,
#form-attachment,
#form-submit,
#form-attachment::file-selector-button {
  font-size: 0.875rem;
}

.todo-form label {
  font-size: 0.75rem;
  color: var(--bs-dark);
}

.todo-form .form-error {
  color: var(--bs-danger);
}

#form-description {
  padding: 0.25rem 0.5rem;
  border: var(--bs-gray-400) solid;
  border-radius: 0.25rem;
}

input:focus,
input:focus-visible,
button:focus {
  outline: 0;
  box-shadow: 0 0 0 0.25rem #0091ff40;
  border-radius: 0.25rem;
}

input {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

input::placeholder {
  font-style: italic;
}

#form-attachment {
  color: transparent;
  user-select: none;
}

#form-attachment::file-selector-button {
  margin-right: 0.5rem;
}

.form-preview-grid {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  overflow: hidden;
  gap: 0.5rem;
}

.form-preview-image {
  width: max(25%, 8rem);
  border: var(--bs-gray-400) solid;
  border-radius: 0.25rem;
  height: 8rem;
  flex-grow: 1;
  overflow: hidden;
  position: relative;
}

.form-preview-image img {
  max-height: 100%;
  min-width: 100%;
  object-fit: cover;
  object-position: center;
}

.form-preview-remove {
  opacity: 0;
  background-color: rgb(0 0 0 / 50%);
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
}

.form-preview-remove:hover,
.form-preview-remove:focus {
  opacity: 1;
  cursor: pointer;
}

.form-preview-remove span {
  color: var(--bs-danger);
  font-size: 4rem;
}

#form-attachment::file-selector-button {
  background-color: var(--bs-secondary);
  border: var(--bs-secondary) solid;
}

#form-submit {
  background-color: var(--noop-primary-color);
  border: var(--noop-primary-color) solid;
}

#form-attachment::file-selector-button,
#form-submit  {
  color: #fff;
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
}

#form-submit {
  margin-left: auto;
}

input[type="file"] {
  font-size: 1rem;
}

input::file-selector-button {
  font-size: 1rem;
}

input::file-selector-button:hover,
input::file-selector-button:focus,
input[type="file"]:focus-visible,
input[type="button"]:hover,
input[type="button"]:focus,
input[type="submit"]:hover,
input[type="submit"]:focus,
button:hover,
button:focus {
  filter: brightness(90%);
  cursor: pointer;
}
</style>
