<script setup>
import DocumentationStatus from "./DocumentationStatus.vue";
import PersonChip from "aleksis.core/components/person/PersonChip.vue";
</script>

<template>
  <div :class="{ 'full-width grid': true, 'large-grid': largeGrid }">
    <div class="d-flex">
      <documentation-status v-if="compact" v-bind="documentationPartProps" />
      <div :class="{ 'text-right d-flex flex-column fit-content': largeGrid }">
        <time :datetime="documentation.datetimeStart" class="text-no-wrap">
          {{ $d(toDateTime(documentation.datetimeStart), "shortTime") }}
        </time>
        <span v-if="!largeGrid">–</span>
        <time :datetime="documentation.datetimeEnd" class="text-no-wrap">
          {{ $d(toDateTime(documentation.datetimeEnd), "shortTime") }}
        </time>
      </div>
    </div>
    <span
      :class="{
        'text-right': !largeGrid,
        'text-subtitle-1': largeGrid,
        'font-weight-medium': largeGrid,
      }"
    >
      {{ documentation.course?.name }}
    </span>
    <div
      :class="{
        'd-flex align-center flex-wrap gap': true,
        'justify-center': largeGrid,
        'justify-start': !largeGrid,
      }"
    >
      <subject-chip
        v-if="documentation.subject"
        :subject="documentation.subject"
        v-bind="compact ? dialogActivator.attrs : {}"
        v-on="compact ? dialogActivator.on : {}"
      />
      <subject-chip
        v-if="
          documentation?.amends?.amends?.subject &&
          documentation.amends.amends.subject.id !== documentation.subject.id
        "
        :subject="documentation.amends.amends.subject"
        v-bind="compact ? dialogActivator.attrs : {}"
        v-on="compact ? dialogActivator.on : {}"
        class="text-decoration-line-through"
        disabled
      />
    </div>
    <div
      :class="{
        'd-flex align-center flex-wrap gap': true,
        'justify-end': !largeGrid,
      }"
    >
      <person-chip
        v-for="teacher in documentation.teachers"
        :key="documentation.id + '-teacher-' + teacher.id"
        :person="teacher"
        :no-link="compact"
        v-bind="compact ? dialogActivator.attrs : {}"
        v-on="compact ? dialogActivator.on : {}"
      />
      <person-chip
        v-for="teacher in amendedTeachers"
        :key="documentation.id + '-amendedTeacher-' + teacher.id"
        :person="teacher"
        :no-link="compact"
        v-bind="compact ? dialogActivator.attrs : {}"
        v-on="compact ? dialogActivator.on : {}"
        class="text-decoration-line-through"
        disabled
      />
    </div>
  </div>
</template>

<script>
import SubjectChip from "aleksis.apps.cursus/components/SubjectChip.vue";
import { DateTime } from "luxon";
import documentationPartMixin from "./documentationPartMixin";

export default {
  name: "LessonInformation",
  mixins: [documentationPartMixin],
  components: {
    SubjectChip,
  },
  methods: {
    toDateTime(dateString) {
      return DateTime.fromISO(dateString);
    },
  },
  computed: {
    largeGrid() {
      return this.compact && !this.$vuetify.breakpoint.mobile;
    },
    amendedTeachers() {
      if (
        this.documentation?.amends?.amends?.teachers &&
        this.documentation.amends.amends.teachers.length
      ) {
        return this.documentation.amends.amends.teachers.filter(
          (at) => !this.documentation.teachers.includes((t) => t.id === at.id),
        );
      }
      return [];
    },
  },
};
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 1em;
  align-content: start;
}

.large-grid {
  grid-template-columns: 1fr 1fr 1fr 1fr;
  align-content: unset;
}

.grid:last-child {
  justify-self: end;
  justify-content: end;
}

.fit-content {
  width: fit-content;
}

.gap {
  gap: 0.25em;
}
</style>
