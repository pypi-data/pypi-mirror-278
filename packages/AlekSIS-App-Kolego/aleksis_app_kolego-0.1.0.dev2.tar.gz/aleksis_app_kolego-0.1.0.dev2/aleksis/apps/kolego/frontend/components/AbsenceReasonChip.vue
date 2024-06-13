<script>
import CounterChip from "aleksis.core/components/generic/chips/CounterChip.vue";

export default {
  name: "AbsenceReasonChip",
  components: { CounterChip },
  props: {
    absenceReason: {
      type: Object,
      required: true,
    },
    short: {
      type: Boolean,
      required: false,
      default: false,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  extends: CounterChip,
  computed: {
    text() {
      return this.short
        ? this.absenceReason.shortName
        : this.absenceReason.name;
    },
  },
};
</script>

<template>
  <counter-chip
    :color="absenceReason.colour"
    :value="absenceReason.id"
    :count="count"
    outlined
    v-bind="$attrs"
    v-on="$listeners"
  >
    <v-avatar left v-if="absenceReason.default">
      <v-tooltip bottom>
        <template #activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on" small> mdi-flare </v-icon>
        </template>
        <span>{{ $t("kolego.absence_reason.default") }}</span>
      </v-tooltip>
    </v-avatar>
    <slot name="prepend" />
    {{ text }}
    <slot name="append" />
    <v-avatar right v-if="loading">
      <v-progress-circular indeterminate :size="16" :width="2" />
    </v-avatar>
  </counter-chip>
</template>
