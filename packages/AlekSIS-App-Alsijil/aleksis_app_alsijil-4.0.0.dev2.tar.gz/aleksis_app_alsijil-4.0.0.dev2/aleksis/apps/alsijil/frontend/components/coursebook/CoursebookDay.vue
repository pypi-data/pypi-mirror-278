<template>
  <v-list-item :style="{ scrollMarginTop: '145px' }" two-line class="px-0">
    <v-list-item-content>
      <v-subheader class="text-h6 px-1">{{
        $d(date, "dateWithWeekday")
      }}</v-subheader>
      <v-list max-width="100%" class="pt-0 mt-n1">
        <v-list-item
          v-for="doc in docs"
          :key="'documentation-' + (doc.oldId || doc.id)"
          class="px-1"
        >
          <documentation-modal
            :documentation="doc"
            :affected-query="lastQuery"
          />
        </v-list-item>
      </v-list>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
import DocumentationModal from "./documentation/DocumentationModal.vue";
export default {
  name: "CoursebookDay",
  components: {
    DocumentationModal,
  },
  props: {
    date: {
      type: Object,
      required: true,
    },
    docs: {
      type: Array,
      required: true,
    },
    lastQuery: {
      type: Object,
      required: true,
    },
    focusOnMount: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  emits: ["init"],
  methods: {
    focus(how) {
      this.$el.scrollIntoView({
        behavior: how,
        block: "start",
        inline: "nearest",
      });
      console.log("focused @", this.date.toISODate());
    },
  },
  mounted() {
    if (this.focusOnMount) {
      this.$nextTick(this.focus("instant"));
      this.$emit("init");
    }
  },
};
</script>
