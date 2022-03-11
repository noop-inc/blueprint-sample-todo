<script setup>
import { ref, unref, watch, onMounted } from 'vue'

const todos = ref([])
const showCreateForm = ref(false)
const formDesciption = ref(null)
const formImages = ref([])
const imageInput = ref(null)
const invalidDesciption = ref(false)
const invalidImageCount = ref(false)
const invalidImageSize = ref(false)
const enlargedImage = ref(null)

const assignImages = () => {
  const files = [...unref(imageInput).files]
  const filterValidSize = files.filter(file => file.size <= 1000000)
  invalidImageSize.value = files.length !== filterValidSize.length
  invalidImageCount.value = (unref(formImages).length + filterValidSize.length) > 6
  const sliceLength = filterValidSize.slice(0, 6 - unref(formImages).length)
  const formattedFiles = sliceLength.map(file => ({
    file,
    key: window.crypto.getRandomValues(new Uint32Array(1))[0],
    src: URL.createObjectURL(file)
  }))
  formImages.value = [...unref(formImages), ...formattedFiles]
  unref(imageInput).value = null
}

const removeImage = idx => {
  invalidImageCount.value = false
  invalidImageSize.value = false
  formImages.value = unref(formImages).filter((_, i) => i !== idx)
}

const clearForm = () => {
  formDesciption.value = null
  formImages.value = []
  invalidDesciption.value = false
  invalidImageCount.value = false
}

const closeModal = () => {
  showCreateForm.value = false
  enlargedImage.value = null
}

watch(showCreateForm, clearForm)

watch([showCreateForm, enlargedImage], () => {
  if (unref(showCreateForm) || unref(enlargedImage)) {
    window.document.body.style.overflow = 'hidden'
  } else {
    window.document.body.style.overflow = null
  }
})

watch(formDesciption, () => {
  if (unref(invalidDesciption)) invalidDesciption.value = false
})

const handleSubmit = async () => {
  if (!unref(formDesciption)) {
    invalidDesciption.value = true
  } else {
    const formData = new FormData()
    formData.append('description', unref(formDesciption))
    unref(formImages).forEach(({ file }) => {
      formData.append('images', file)
    })

    const res = await fetch(
      '/api/todos',
      {
        method: 'POST',
        body: formData
      }
    )
    const data = await res.json()
    todos.value = [...unref(todos), data]
    showCreateForm.value = false
  }
}

const getAllTodos = async () => {
  const res = await fetch('/api/todos')
  const data = await res.json()
  todos.value = data.sort((a, b) => a.created - b.created)
}

onMounted(() => {
  getAllTodos()
})
</script>

<template>
  <header class="todo-header">
    <h1>
      <a
        class="form-link"
        href="https://noop.dev"
        target="_blank"
      >
        <img
          alt="Noop"
          src="./assets/logo.svg"
        >
      </a>
      <span>{{ 'Todo Sample Application' }}</span>
    </h1>
  </header>
  <template v-if="todos.length">
    <hr class="divider">
    <section class="todo-list">
      <div
        v-for="{ description, images, id, completed } in todos"
        :key="id"
        class="todo-item"
      >
        {{ completed }}
        {{ description }}
        <div
          v-if="images.length"
          class="image-preview-grid"
        >
          <span
            v-for="key in images"
            :key="key"
            class="image-preview-item"
          >
            <img :src="`/api/images/${key}`">
            <button
              type="button"
              class="form-button image-preview-button"
              title="Enlarge Image"
              @click.prevent="enlargedImage = key"
            />
          </span>
        </div>
      </div>
    </section>
  </template>
  <hr class="divider">
  <section class="todo-create">
    <div>
      <button
        class="form-button"
        @click="showCreateForm = true"
      >
        {{ 'New Todo' }}
      </button>
    </div>
  </section>
  <section
    v-if="enlargedImage || showCreateForm"
    class="todo-modal"
    @click="closeModal"
  >
    <div
      v-if="enlargedImage"
      class="enlarged-image"
      @click.stop
    >
      <img :src="`/api/images/${enlargedImage}`">
    </div>
    <form
      v-if="showCreateForm"
      class="todo-form"
      @submit.prevent="handleSubmit"
      @click.stop
    >
      <div class="todo-form-row">
        <h5 class="todo-form-header">
          <button
            class="form-button todo-close"
            title="Close modal"
            type="button"
            @click="closeModal"
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
          class="form-input"
          type="text"
          autocomplete="off"
          placeholder="What needs to be done?"
        >
        <label
          v-if="invalidDesciption"
          class="form-error"
        >Todo description is required</label>
      </div>
      <div class="todo-form-row">
        <label for="form-file">Attach Images (optional)</label>
        <input
          id="form-file"
          ref="imageInput"
          class="form-input"
          type="file"
          multiple
          accept="image/*"
          @input="assignImages"
        >
        <label
          v-if="invalidImageCount"
          class="form-error"
        >Maximum of 6 images can be attached</label>
        <label
          v-if="invalidImageSize"
          class="form-error"
        >Images must be under 1MB</label>
        <div
          v-if="formImages.length"
          class="image-preview-grid"
        >
          <span
            v-for="({ src, key }, idx) in formImages"
            :key="key"
            class="image-preview-item"
          >
            <img :src="src">
            <button
              type="button"
              class="form-button image-preview-button"
              title="Remove Image"
              @click.prevent="removeImage(idx)"
            >
              <span>
                {{ '×' }}
              </span>
            </button>
          </span>
        </div>
      </div>
      <hr class="divider">
      <div class="todo-form-row">
        <button
          id="form-submit"
          class="form-button"
          type="submit"
        >
          {{ 'Create Todo' }}
        </button>
      </div>
    </form>
  </section>
</template>

<style>
@import './reboot.css';

:root {
  --noop-primary-color: #0091ff;
  --noop-bg-color: #f4f3ef;
  --noop-dark-color: #212120;
}

body {
  background-color: var(--noop-dark-color);
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
  margin: auto;
}

.todo-list {
  max-width: 640px;
  flex-grow: 1;
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

.todo-header {
  background-color: var(--noop-dark-color);
}

.todo-header h1 {
  text-align: center;
  color: var(--bs-white);
  margin-bottom: 0;
  font-weight: 200;
  letter-spacing: 0.0125em
}

.todo-header h1 a {
  float: right;
  display: flex;
}

.todo-header h1 a img {
  height: 1.2em;
  width: 1.2em;
}

.todo-header h1 span {
  padding: 0 0.25rem 0 calc(1.2em + 0.25rem);
}

.todo-list .todo-item {
  background-color: #fff;
  padding: 1rem;
  border: var(--bs-gray-400) solid 1px;
  display: flex;
  flex-direction: column;
}

.todo-list .todo-item .image-preview-button {
  cursor: zoom-in;
}

.todo-list .todo-item:first-child {
  border-top-left-radius: 0.25rem;
  border-top-right-radius: 0.25rem;
}

.todo-list .todo-item:last-child {
  border-bottom-left-radius: 0.25rem;
  border-bottom-right-radius: 0.25rem;
}

.todo-list .todo-item:not(:last-child) {
  border-bottom: none;
}

.todo-modal {
  position: fixed;
  padding: 1rem;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgb(0 0 0 / 50%);
  display: flex;
  overflow: hidden;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.enlarged-image {
  border: var(--bs-gray-400) solid;
  border-radius: 0.25rem;
  position: relative;
  max-height: calc(100vh - 2rem);
  max-width: calc(100vw - 2rem);
}

.enlarged-image img {
  max-height: 100%;
  max-width: 100%;
  border-radius: 0.125rem;
  object-fit: contain;
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
  user-select: none;
}

.todo-form-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

#form-description,
#form-file,
#form-submit,
#form-file::file-selector-button {
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

input.form-input:focus,
input.form-input:focus-visible,
button:focus,
a.form-link:focus {
  outline: 0;
  box-shadow: 0 0 0 0.25rem #0091ff40;
  border-radius: 0.25rem;
}

input.form-input {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

input.form-input::placeholder {
  font-style: italic;
}

#form-file {
  color: transparent;
  user-select: none;
}

#form-file::file-selector-button {
  margin-right: 0.5rem;
}

.image-preview-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.image-preview-item {
  border: var(--bs-gray-400) solid;
  border-radius: 0.25rem;
  min-width: 6rem;
  height: 8rem;
  flex-grow: 1;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.image-preview-item img {
  max-height: 100%;
  min-width: 100%;
  flex: 1;
  border-radius: 0.125rem;
  object-fit: cover;
}

.image-preview-button {
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
  padding: 0;
  border-radius: 0.125rem;
}

.image-preview-button:hover,
.image-preview-button:focus {
  opacity: 1;
  cursor: pointer;
}

.image-preview-button span {
  color: var(--bs-danger);
  font-size: 4rem;
  user-select: none;
}

#form-file::file-selector-button {
  background-color: var(--bs-secondary);
  border: var(--bs-secondary) solid;
}

#form-submit {
  background-color: var(--noop-primary-color);
  border: var(--noop-primary-color) solid;
}

#form-file::file-selector-button,
#form-submit  {
  color: #fff;
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
}

#form-submit {
  margin-left: auto;
}

input.form-input[type="file"] {
  font-size: 1rem;
}

input.form-input::file-selector-button {
  font-size: 1rem;
}

button.form-button {
  user-select: none;
}

input.form-input::file-selector-button:hover,
input.form-input::file-selector-button:focus,
input.form-input[type="file"]:focus-visible,
button.form-button:hover,
button.form-button:focus,
a.form-link:hover,
a.form-link:focus {
  filter: brightness(90%);
  cursor: pointer;
}
</style>
