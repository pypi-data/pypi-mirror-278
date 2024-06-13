<template>
  <c-r-u-d-iterator
    i18n-key="alsijil.coursebook"
    :gql-query="gqlQuery"
    :gql-additional-query-args="gqlQueryArgs"
    :enable-create="false"
    :enable-edit="false"
    :elevated="false"
    @lastQuery="lastQuery = $event"
    ref="iterator"
    fixed-header
    disable-pagination
    hide-default-footer
    use-deep-search
  >
    <template #additionalActions="{ attrs, on }">
      <coursebook-filters v-model="filters" />
    </template>
    <template #default="{ items }">
      <coursebook-loader />
      <coursebook-day
        v-for="{ date, docs, first, last } in groupDocsByDay(items)"
        v-intersect="{
          handler: intersectHandler(date, first, last),
          options: {
            rootMargin: '-' + topMargin + 'px 0px 0px 0px',
            threshold: [0, 1],
          },
        }"
        :date="date"
        :docs="docs"
        :lastQuery="lastQuery"
        :focus-on-mount="initDate && initDate.toMillis() === date.toMillis()"
        @init="transition"
        :key="'day-' + date"
        ref="days"
      />
      <coursebook-loader />

      <date-select-footer
        :value="currentDate"
        @input="gotoDate"
        @prev="gotoPrev"
        @next="gotoNext"
      />
    </template>
    <template #loading>
      <coursebook-loader :number-of-days="10" :number-of-docs="5" />
    </template>

    <template #no-data>
      <CoursebookEmptyMessage icon="mdi-book-off-outline">
        {{ $t("alsijil.coursebook.no_data") }}
      </CoursebookEmptyMessage>
    </template>

    <template #no-results>
      <CoursebookEmptyMessage icon="mdi-book-alert-outline">
        {{
          $t("alsijil.coursebook.no_results", { search: $refs.iterator.search })
        }}
      </CoursebookEmptyMessage>
    </template>
  </c-r-u-d-iterator>
</template>

<script>
import CRUDIterator from "aleksis.core/components/generic/CRUDIterator.vue";
import DateSelectFooter from "aleksis.core/components/generic/DateSelectFooter.vue";
import CoursebookDay from "./CoursebookDay.vue";
import { DateTime, Interval } from "luxon";
import { documentationsForCoursebook } from "./coursebook.graphql";
import CoursebookFilters from "./CoursebookFilters.vue";
import CoursebookLoader from "./CoursebookLoader.vue";
import CoursebookEmptyMessage from "./CoursebookEmptyMessage.vue";

export default {
  name: "Coursebook",
  components: {
    CoursebookEmptyMessage,
    CoursebookFilters,
    CoursebookLoader,
    CRUDIterator,
    DateSelectFooter,
    CoursebookDay,
  },
  props: {
    filterType: {
      type: String,
      required: true,
    },
    objId: {
      type: [Number, String],
      required: false,
      default: null,
    },
    objType: {
      type: String,
      required: false,
      default: null,
    },
    /**
     * Number of consecutive to load at once
     * This number of days is initially loaded and loaded
     * incrementally while scrolling.
     */
    dayIncrement: {
      type: Number,
      required: false,
      default: 7,
    },
    /**
     * Margin from coursebook list to top of viewport in pixels
     */
    topMargin: {
      type: Number,
      required: false,
      default: 165,
    },
  },
  data() {
    return {
      gqlQuery: documentationsForCoursebook,
      lastQuery: null,
      dateStart: "",
      dateEnd: "",
      // Placeholder values while query isn't completed yet
      groups: [],
      courses: [],
      incomplete: false,
      ready: false,
      initDate: false,
      currentDate: "",
      hashUpdater: false,
    };
  },
  computed: {
    // Assertion: Should only fire on page load or selection change.
    //            Resets date range.
    gqlQueryArgs() {
      return {
        own: this.filterType === "all" ? false : true,
        objId: this.objId ? Number(this.objId) : undefined,
        objType: this.objType?.toUpperCase(),
        dateStart: this.dateStart,
        dateEnd: this.dateEnd,
        incomplete: !!this.incomplete,
      };
    },
    filters: {
      get() {
        return {
          objType: this.objType,
          objId: this.objId,
          filterType: this.filterType,
          incomplete: this.incomplete,
        };
      },
      set(selectedFilters) {
        if (Object.hasOwn(selectedFilters, "incomplete")) {
          this.incomplete = selectedFilters.incomplete;
        } else if (
          Object.hasOwn(selectedFilters, "filterType") ||
          Object.hasOwn(selectedFilters, "objId") ||
          Object.hasOwn(selectedFilters, "objType")
        ) {
          this.$router.push({
            name: "alsijil.coursebook",
            params: {
              filterType: selectedFilters.filterType
                ? selectedFilters.filterType
                : this.filterType,
              objType: selectedFilters.objType,
              objId: selectedFilters.objId,
            },
            hash: this.$route.hash,
          });
          // computed should not have side effects
          // but this was actually done before filters was refactored into
          // its own component
          this.resetDate();
          // might skip query until both set = atomic
        }
      },
    },
  },
  methods: {
    resetDate(toDate) {
      // Assure current date
      console.log("Resetting date range", this.$route.hash);
      this.currentDate = toDate || this.$route.hash?.substring(1);
      if (!this.currentDate) {
        console.log("Set default date");
        this.setDate(DateTime.now().toISODate());
      }

      const date = DateTime.fromISO(this.currentDate);
      this.initDate = date;
      this.dateStart = date.minus({ days: this.dayIncrement }).toISODate();
      this.dateEnd = date.plus({ days: this.dayIncrement }).toISODate();
    },
    transition() {
      this.initDate = false;
      this.ready = true;
    },
    groupDocsByDay(docs) {
      // => {dt: {date: dt, docs: doc ...} ...}
      const docsByDay = docs.reduce((byDay, doc) => {
        // This works with dummy. Does actual doc have dateStart instead?
        const day = DateTime.fromISO(doc.datetimeStart).startOf("day");
        byDay[day] ??= { date: day, docs: [] };
        byDay[day].docs.push(doc);
        return byDay;
      }, {});
      // => [{date: dt, docs: doc ..., idx: idx, lastIdx: last-idx} ...]
      // sorting is necessary since backend can send docs unordered
      return Object.keys(docsByDay)
        .sort()
        .map((key, idx, { length }) => {
          const day = docsByDay[key];
          day.first = idx === 0;
          const lastIdx = length - 1;
          day.last = idx === lastIdx;
          return day;
        });
    },
    // docsByDay: {dt: [dt doc ...] ...}
    fetchMore(from, to, then) {
      console.log("fetching", from, to);
      this.lastQuery.fetchMore({
        variables: {
          dateStart: from,
          dateEnd: to,
        },
        // Transform the previous result with new data
        updateQuery: (previousResult, { fetchMoreResult }) => {
          console.log("Received more");
          then();
          return { items: previousResult.items.concat(fetchMoreResult.items) };
        },
      });
    },
    setDate(date) {
      this.currentDate = date;
      if (!this.hashUpdater) {
        this.hashUpdater = window.requestIdleCallback(() => {
          if (!(this.$route.hash.substring(1) === this.currentDate)) {
            this.$router.replace({ hash: this.currentDate });
          }
          this.hashUpdater = false;
        });
      }
    },
    fixScrollPos(height, top) {
      this.$nextTick(() => {
        if (height < document.documentElement.scrollHeight) {
          document.documentElement.scrollTop =
            document.documentElement.scrollHeight - height + top;
          this.ready = true;
        } else {
          // Update top, could have changed in the meantime.
          this.fixScrollPos(height, document.documentElement.scrollTop);
        }
      });
    },
    intersectHandler(date, first, last) {
      let once = true;
      return (entries) => {
        const entry = entries[0];
        if (entry.isIntersecting) {
          if (entry.boundingClientRect.top <= this.topMargin || first) {
            console.log("@ ", date.toISODate());
            this.setDate(date.toISODate());
          }

          if (once && this.ready && first) {
            console.log("load up", date.toISODate());
            this.ready = false;
            this.fetchMore(
              date.minus({ days: this.dayIncrement }).toISODate(),
              date.minus({ days: 1 }).toISODate(),
              () => {
                this.fixScrollPos(
                  document.documentElement.scrollHeight,
                  document.documentElement.scrollTop,
                );
              },
            );
            once = false;
          } else if (once && this.ready && last) {
            console.log("load down", date.toISODate());
            this.ready = false;
            this.fetchMore(
              date.plus({ days: 1 }).toISODate(),
              date.plus({ days: this.dayIncrement }).toISODate(),
              () => {
                this.ready = true;
              },
            );
            once = false;
          }
        }
      };
    },
    // Improve me?
    // The navigation logic could be a bit simpler if the current days
    // where known as a sorted array (= result of groupDocsByDay) But
    // then the list would need its own component and this gets rather
    // complicated. Then the calendar could also show the present days
    // / gray out the missing.
    //
    // Next two: arg date is ts object
    findPrev(date) {
      return this.$refs.days
        .map((day) => day.date)
        .sort()
        .reverse()
        .find((date2) => date2 < date);
    },
    findNext(date) {
      return this.$refs.days
        .map((day) => day.date)
        .sort()
        .find((date2) => date2 > date);
    },
    gotoDate(date) {
      const present = this.$refs.days.find(
        (day) => day.date.toISODate() === date,
      );

      if (present) {
        // React immediatly -> smoother navigation
        // Also intersect handler does not always react to scrollIntoView
        this.setDate(date);
        present.focus("smooth");
      } else {
        const prev = this.findPrev(DateTime.fromISO(date));
        const next = this.findNext(DateTime.fromISO(date));
        if (prev && next) {
          // In between two present days -> goto prev
          this.gotoDate(prev.toISODate());
        } else {
          // Outsite present day range
          this.resetDate(date);
        }
      }
    },
    gotoPrev() {
      const prev = this.findPrev(DateTime.fromISO(this.currentDate));
      if (prev) {
        this.gotoDate(prev.toISODate());
      }
    },
    gotoNext() {
      const next = this.findNext(DateTime.fromISO(this.currentDate));
      if (next) {
        this.gotoDate(next.toISODate());
      }
    },
  },
  created() {
    this.resetDate();
  },
};
</script>

<style>
.max-width {
  max-width: 25rem;
}
</style>
