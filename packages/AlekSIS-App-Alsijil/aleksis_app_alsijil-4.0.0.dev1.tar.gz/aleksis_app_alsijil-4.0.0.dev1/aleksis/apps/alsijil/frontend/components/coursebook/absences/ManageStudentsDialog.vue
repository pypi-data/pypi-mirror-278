<script>
import AbsenceReasonButtons from "aleksis.apps.kolego/components/AbsenceReasonButtons.vue";
import AbsenceReasonChip from "aleksis.apps.kolego/components/AbsenceReasonChip.vue";
import AbsenceReasonGroupSelect from "aleksis.apps.kolego/components/AbsenceReasonGroupSelect.vue";
import CancelButton from "aleksis.core/components/generic/buttons/CancelButton.vue";
import MobileFullscreenDialog from "aleksis.core/components/generic/dialogs/MobileFullscreenDialog.vue";
import mutateMixin from "aleksis.core/mixins/mutateMixin.js";
import documentationPartMixin from "../documentation/documentationPartMixin";
import LessonInformation from "../documentation/LessonInformation.vue";
import { updateParticipationStatuses } from "./participationStatus.graphql";
import SlideIterator from "aleksis.core/components/generic/SlideIterator.vue";

export default {
  name: "ManageStudentsDialog",
  extends: MobileFullscreenDialog,
  components: {
    AbsenceReasonChip,
    AbsenceReasonGroupSelect,
    AbsenceReasonButtons,
    CancelButton,
    LessonInformation,
    MobileFullscreenDialog,
    SlideIterator,
  },
  mixins: [documentationPartMixin, mutateMixin],
  data() {
    return {
      dialog: false,
      search: "",
      loadSelected: false,
      selected: [],
      isExpanded: false,
    };
  },
  props: {
    loadingIndicator: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
  computed: {
    items() {
      return this.documentation.participations;
    },
  },
  methods: {
    sendToServer(participations, field, value) {
      if (field !== "absenceReason") return;

      this.mutate(
        updateParticipationStatuses,
        {
          input: participations.map((participation) => ({
            id: participation.id,
            absenceReason: value === "present" ? null : value,
          })),
        },
        (storedDocumentations, incomingStatuses) => {
          const documentation = storedDocumentations.find(
            (doc) => doc.id === this.documentation.id,
          );

          incomingStatuses.forEach((newStatus) => {
            const participationStatus = documentation.participations.find(
              (part) => part.id === newStatus.id,
            );
            participationStatus.absenceReason = newStatus.absenceReason;
            participationStatus.isOptimistic = newStatus.isOptimistic;
          });

          return storedDocumentations;
        },
      );
    },
    handleMultipleAction(absenceReasonId) {
      this.loadSelected = true;
      this.sendToServer(this.selected, "absenceReason", absenceReasonId);
      this.$once("save", this.resetMultipleAction);
    },
    resetMultipleAction() {
      this.loadSelected = false;
      this.$set(this.selected, []);
      this.$refs.iterator.selected = [];
    },
  },
};
</script>

<template>
  <mobile-fullscreen-dialog
    scrollable
    v-bind="$attrs"
    v-on="$listeners"
    v-model="dialog"
  >
    <template #activator="activator">
      <slot name="activator" v-bind="activator" />
    </template>

    <template #title>
      <lesson-information v-bind="documentationPartProps" :compact="false" />
      <v-scroll-x-transition leave-absolute>
        <v-text-field
          v-show="!isExpanded"
          type="search"
          v-model="search"
          clearable
          rounded
          hide-details
          single-line
          prepend-inner-icon="$search"
          dense
          outlined
          :placeholder="$t('actions.search')"
          class="pt-4 full-width"
        />
      </v-scroll-x-transition>
      <v-scroll-x-transition>
        <div v-show="selected.length > 0" class="full-width mt-4">
          <absence-reason-buttons
            allow-empty
            empty-value="present"
            @input="handleMultipleAction"
          />
        </div>
      </v-scroll-x-transition>
    </template>
    <template #content>
      <slide-iterator
        ref="iterator"
        v-model="selected"
        :items="items"
        :search="search"
        :item-key-getter="
          (item) => 'documentation-' + documentation.id + '-student-' + item.id
        "
        :is-expanded.sync="isExpanded"
        :loading="loadingIndicator || loadSelected"
        :load-only-selected="loadSelected"
        :disabled="loading"
      >
        <template #listItemContent="{ item }">
          <v-list-item-title>
            {{ item.person.fullName }}
          </v-list-item-title>
          <v-list-item-subtitle v-if="item.absenceReason">
            <absence-reason-chip small :absence-reason="item.absenceReason" />
          </v-list-item-subtitle>
        </template>

        <template #expandedItem="{ item, close }">
          <v-card-title>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn v-bind="attrs" v-on="on" icon @click="close">
                  <v-icon>$prev</v-icon>
                </v-btn>
              </template>
              <span v-t="'actions.back_to_overview'" />
            </v-tooltip>
            {{ item.person.fullName }}
          </v-card-title>
          <v-card-text>
            <absence-reason-group-select
              allow-empty
              empty-value="present"
              :loadSelectedChip="loading"
              :value="item.absenceReason?.id || 'present'"
              @input="sendToServer([item], 'absenceReason', $event)"
            />
          </v-card-text>
        </template>
      </slide-iterator>
    </template>

    <template #actions>
      <cancel-button
        @click="dialog = false"
        i18n-key="actions.close"
        v-show="$vuetify.breakpoint.mobile"
      />
    </template>
  </mobile-fullscreen-dialog>
</template>

<style scoped></style>
