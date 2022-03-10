<script setup>
import { ref, unref, watch } from 'vue'

const showModal = ref(false)
const formDesciption = ref(null)
const formAttachment = ref(null)
const attachmentInput = ref(null)

const clearAttachment = () => {
  if (unref(attachmentInput)) unref(attachmentInput).value = null
  formAttachment.value = null
}

watch(showModal, () => {
  formDesciption.value = null
  clearAttachment()
})

// const res = await fetch(
//   'https://blueprint.local.noop.app/api/todos',
//   {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({
//       description: 'foo bar'
//     })
//   }
// )
// const { data } = await res.json()

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
      enctype="multipart/form-data"
      method="post"
      @click.stop
    >
      <div>
        <h5 class="todo-form-header">
          <button
            class="todo-close"
            title="Close modal"
            @click="showModal = false"
          >
            {{ '×' }}
          </button>
          <span>{{ 'Provide Todo Details…' }}</span>
        </h5>
      </div>
      <hr class="divider">
      <div>
        <label for="form-description">Description (required)</label>
        <input
          id="form-description"
          v-model="formDesciption"
          type="text"
          autocomplete="off"
          placeholder="What needs to be done?"
        >
      </div>
      <div>
        <label for="form-attachment">Attachment (optional, PNG or JPG, 2MB max)</label>
        <span>
          <input
            id="form-attachment"
            ref="attachmentInput"
            type="file"
            accept=".jpg, .jpeg, .png"
            @change="formAttachment = $event"
          >
          <button
            v-if="formAttachment"
            title="Remove attachment"
            class="form-remove"
            @click.stop.prevent="clearAttachment"
          >
            {{ '×' }}
          </button>
        </span>
      </div>
      <hr class="divider">
      <div>
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
  font-size: 0.75em;
  font-family: 'Brush Script MT', cursive;
  letter-spacing: 1px;
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

.todo-form div {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.todo-form div span {
  display: flex;
  align-items: center;
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
  flex: 1;
}

.form-remove {
  font-size: 1.25rem;
  color: var(--bs-danger);
  display: flex;
  align-items: center;
  margin-right: -0.5rem;
  padding: 0 0.5rem;
  cursor: pointer;
  border: none;
  background: none;
}

#form-attachment::file-selector-button {
  margin-right: 0.5rem;
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
