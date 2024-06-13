<script setup>
import AbsenceReasonChip from "aleksis.apps.kolego/components/AbsenceReasonChip.vue";
</script>

<template>
  <div
    class="d-flex align-center justify-space-between justify-md-end flex-wrap gap"
  >
    <v-chip dense color="success" outlined v-if="total > 0">
      {{ $t("alsijil.coursebook.present_number", { present, total }) }}
    </v-chip>
    <absence-reason-chip
      v-for="[reasonId, participations] in Object.entries(absences)"
      :key="'reason-' + reasonId"
      :absence-reason="participations[0].absenceReason"
      dense
    >
      <template #append>
        <span
          >:
          <span>
            {{
              participations
                .slice(0, 5)
                .map((participation) => participation.person.firstName)
                .join(", ")
            }}
          </span>
          <span v-if="participations.length > 5">
            <!-- eslint-disable @intlify/vue-i18n/no-raw-text -->
            +{{ participations.length - 5 }}
            <!-- eslint-enable @intlify/vue-i18n/no-raw-text -->
          </span>
        </span>
      </template>
    </absence-reason-chip>

    <manage-students-trigger v-bind="documentationPartProps" />
  </div>
</template>

<script>
import documentationPartMixin from "./documentationPartMixin";
import ManageStudentsTrigger from "../absences/ManageStudentsTrigger.vue";

export default {
  name: "LessonNotes",
  components: { ManageStudentsTrigger },
  mixins: [documentationPartMixin],
  computed: {
    total() {
      return this.documentation.participations.length;
    },
    present() {
      return this.documentation.participations.filter(
        (p) => p.absenceReason === null,
      ).length;
    },
    absences() {
      // Get all course attendants who have an absence reason
      return Object.groupBy(
        this.documentation.participations.filter(
          (p) => p.absenceReason !== null,
        ),
        ({ absenceReason }) => absenceReason.id,
      );
    },
  },
};
</script>

<style scoped>
.gap {
  gap: 0.25em;
}
</style>
