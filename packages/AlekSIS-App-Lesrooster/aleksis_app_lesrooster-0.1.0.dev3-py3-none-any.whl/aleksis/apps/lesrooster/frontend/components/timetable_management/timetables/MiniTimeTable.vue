<script>
import { defineComponent } from "vue";
import { slots } from "../../breaks_and_slots/slot.graphql";
import LessonCard from "../LessonCard.vue";
import MessageBox from "aleksis.core/components/generic/MessageBox.vue";

export default defineComponent({
  name: "MiniTimeTable",
  components: { LessonCard, MessageBox },
  props: {
    timeGrid: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      periods: [],
      weekdays: [],
      slots: [],
    };
  },
  apollo: {
    slots: {
      query: slots,
      variables() {
        return {
          filters: JSON.stringify({
            time_grid: this.timeGrid.id,
          }),
        };
      },
      skip() {
        return this.timeGrid === null;
      },
      update: (data) => data.items,
      result({ data: { items } }) {
        this.weekdays = Array.from(
          new Set(
            items
              .filter((slot) => slot.model === "Slot")
              .map((slot) => slot.weekday),
          ),
        );
        this.periods = Array.from(
          new Set(
            items
              .filter((slot) => slot.model === "Slot")
              .map((slot) => slot.period),
          ),
        );
      },
    },
  },
  computed: {
    gridTemplate() {
      return (
        "[legend-row] auto " +
        this.periods.map((period) => `[period-${period}] auto `).join("") +
        "/ [legend-day] auto" +
        this.weekdays.map((weekday) => ` [${weekday}] 1fr`).join("")
      );
    },
    lessons() {
      return [];
    },
    lessonsPerSlot() {
      let weekdayPeriodSlots = Object.fromEntries(
        this.weekdays.map((weekday) => [
          weekday,
          Object.fromEntries(this.periods.map((period) => [period, []])),
        ]),
      );

      this.lessons?.forEach((lesson) => {
        const weekdayStart = lesson.slotStart.weekday;
        const weekdayEnd = lesson.slotEnd.weekday;
        const periodStart = lesson.slotStart.period;
        const periodEnd = lesson.slotEnd.period;

        // If lesson start and end is on the same day, just add it in between the periods
        if (weekdayStart === weekdayEnd) {
          this.periods.map((period) => {
            if (period <= periodEnd && period >= periodStart) {
              weekdayPeriodSlots[weekdayStart][period].push(lesson);
            }
          });
        } else {
          // this is more complicated.
          // As it is currently not possible to create timetables like this, we will just ignore it
        }
      });

      return weekdayPeriodSlots;
    },
  },
  methods: {
    styleForWeekdayAndPeriod(weekday, period) {
      return {
        gridArea: `period-${period} / ${weekday} / ` + `span 1 / ${weekday}`,
      };
    },
  },
});
</script>

<template>
  <div class="timetable">
    <!-- Empty div to fill top-left corner -->
    <div></div>
    <v-card
      v-for="period in periods"
      :style="{
        gridColumn: 'legend-day',
        gridRow: `period-${period} / span 1`,
      }"
      :key="'period' + period"
    >
      <v-card-text>{{ period }}</v-card-text>
    </v-card>
    <v-card
      v-for="weekday in weekdays"
      :style="{ gridRow: 'legend-row', gridColumn: `${weekday} / span 1` }"
      :key="weekday"
    >
      <v-card-text>{{ $t("weekdays." + weekday) }}</v-card-text>
    </v-card>
    <template v-for="weekday in weekdays">
      <div
        v-for="period in periods"
        :key="'lesson-container-' + weekday + '-' + period"
        :style="styleForWeekdayAndPeriod(weekday, period)"
        class="d-flex flex-column gap-small"
      >
        <lesson-card
          v-for="lesson in lessonsPerSlot[weekday][period]"
          :lesson="lesson"
          :key="lesson.id"
          one-line
        />
      </div>
    </template>

    <message-box type="info" v-if="!lessons || lessons.length === 0">
      {{ $t("lesrooster.timetable_management.no_lessons") }}
    </message-box>
    <message-box type="warning" v-if="!slots || slots.length === 0">
      {{ $t("lesrooster.timetable_management.no_slots") }}
    </message-box>
  </div>
</template>

<style scoped>
.timetable {
  display: grid;
  grid-template: v-bind(gridTemplate);
  gap: 0.7em;
}

.timetable > * {
  width: 100%;
  height: 100%;
}

.gap-small {
  gap: 0.15em;
}
</style>
