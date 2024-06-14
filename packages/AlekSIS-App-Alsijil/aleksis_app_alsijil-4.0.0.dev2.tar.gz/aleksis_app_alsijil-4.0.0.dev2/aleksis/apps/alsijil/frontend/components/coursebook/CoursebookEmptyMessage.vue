<template>
  <v-list-item>
    <v-list-item-content
      class="d-flex justify-center align-center flex-column full-width"
    >
      <div class="mb-4">
        <v-icon large color="primary">{{ icon }}</v-icon>
      </div>
      <v-list-item-title>
        <slot></slot>
      </v-list-item-title>
    </v-list-item-content>
  </v-list-item>
</template>
<script>
export default {
  name: "CoursebookEmptyMessage",
  props: {
    icon: {
      type: String,
      default: "mdi-book-alert-outline",
    },
  },
};
</script>
