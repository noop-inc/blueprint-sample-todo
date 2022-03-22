<script setup>
import { ref, unref, watch, onMounted } from 'vue'
import {
  fetchAllTodos,
  createTodo,
  updateTodo,
  deleteTodo
} from './api.js'

const todos = ref([])
const createForm = ref(false)
const formDescription = ref(null)
const formImages = ref([])
const imageInput = ref(null)
const invalidDescription = ref(false)
const invalidImageCount = ref(false)
const invalidImageSize = ref(false)
const enlargedImage = ref(null)
const editId = ref(null)

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
  formDescription.value = null
  formImages.value = []
  invalidDescription.value = false
  invalidImageCount.value = false
}

const closeModal = () => {
  createForm.value = false
  enlargedImage.value = null
}

document.addEventListener('keyup', (e) => {
  if (e.key === 'Escape') closeModal()
})

watch(createForm, clearForm)

watch([createForm, enlargedImage], () => {
  if (unref(createForm) || unref(enlargedImage)) {
    window.document.body.style.overflow = 'hidden'
  } else {
    window.document.body.style.overflow = null
  }
})

watch(formDescription, () => {
  if (unref(invalidDescription)) invalidDescription.value = false
})

const editToggle = id => {
  const currentTodo = unref(todos).find(todo => todo.id === id)
  const input = window.document.getElementById(`edit-description-${id}`)
  input.value = currentTodo.description
  editId.value = id
  window.setTimeout(() => {
    input.focus()
  }, 0)
}

const handleFetchAllTodos = async () => {
  const allTodo = await fetchAllTodos()
  todos.value = allTodo.sort((a, b) => a.created - b.created)
}

const handleUpdateTodo = async item => {
  const updatedTodo = await updateTodo(item)
  todos.value = unref(todos).map(todo => todo.id === updatedTodo.id ? updatedTodo : todo)
}

const handleDeleteTodo = async id => {
  const deletedTodo = await deleteTodo(id)
  todos.value = unref(todos).filter(todo => todo.id !== deletedTodo.id)
}

const handleSubmit = async e => {
  e.preventDefault()
  if (!unref(formDescription)?.trim()) {
    invalidDescription.value = true
  } else {
    const item = [
      ['description', unref(formDescription)?.trim()],
      ...unref(formImages).map(({ file }) =>
        ['image', file]
      )
    ]
    const newTodo = await createTodo(item)
    todos.value = [...unref(todos), newTodo]
    createForm.value = false
  }
}

const handleEdit = async () => {
  const currentTodo = unref(todos).find(todo => todo.id === unref(editId))
  const input = window.document.getElementById(`edit-description-${currentTodo.id}`)
  const value = input.value?.trim()
  if (value) {
    if (value !== currentTodo.description) {
      await handleUpdateTodo({ id: currentTodo.id, description: value })
    }
    editId.value = null
  }
}

onMounted(async () => {
  await handleFetchAllTodos()
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
      <span>{{ 'Todo Application' }}</span>
      <button
        class="form-button"
        title="New Todo"
        @click="createForm = true"
      >
        {{ 'New Todo' }}
      </button>
    </h1>
  </header>
  <section
    v-if="todos.length"
    class="todo-list"
  >
    <div
      v-for="{ description, images, id, completed } in todos"
      :key="id"
      class="todo-item"
    >
      <div class="todo-description">
        <button
          type="button"
          :class="['form-button todo-complete', { completed }]"
          title="Toggle Complete"
          @click.prevent="handleUpdateTodo({ id, completed: !completed })"
        >
          <span>{{ '✓' }}</span>
        </button>
        <button
          type="button"
          class="form-button todo-delete"
          title="Delete"
          @click.prevent="handleDeleteTodo(id)"
        >
          <span>{{ '×' }}</span>
        </button>
        <div
          :class="{ completed }"
          @dblclick.prevent.stop="editToggle(id)"
        >
          <form
            :class="['edit-form', { 'display-none': editId !== id }]"
            @submit.prevent="handleEdit"
            @click.stop
          >
            <input
              :id="`edit-description-${id}`"
              placeholder="What needs to be completed?"
              class="form-input edit-description"
              type="text"
              autocomplete="off"
              @blur="editId = null"
            >
            <input
              type="submit"
              class="display-none"
            >
          </form>
          <span :class="{ 'display-none': editId === id }">{{ description }}</span>
        </div>
      </div>
      <div
        v-if="images && images.length"
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
  <section
    v-if="enlargedImage || createForm"
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
      v-if="createForm"
      class="todo-form"
      @submit="handleSubmit"
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
        <label for="form-description">
          {{ 'Description (required)' }}
        </label>
        <input
          id="form-description"
          v-model="formDescription"
          class="form-input"
          type="text"
          autocomplete="off"
          placeholder="What needs to be completed?"
        >
        <label
          v-if="invalidDescription"
          class="form-error"
        >
          {{ 'Todo description is required' }}
        </label>
      </div>
      <div class="todo-form-row">
        <label for="form-file">
          {{ 'Attach up to 6 images, 1MB max each (optional)' }}
        </label>
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
        >
          {{ 'Maximum of 6 images can be attached' }}
        </label>
        <label
          v-if="invalidImageSize"
          class="form-error"
        >
          {{ 'Images must be under 1MB' }}
        </label>
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
          title="Create Todo"
        >
          {{ 'Create Todo' }}
        </button>
      </div>
    </form>
  </section>
</template>
