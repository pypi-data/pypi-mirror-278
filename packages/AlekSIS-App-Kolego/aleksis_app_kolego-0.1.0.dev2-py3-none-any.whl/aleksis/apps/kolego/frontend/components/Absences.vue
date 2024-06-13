<script setup>
import AbsenceReasonChip from "./AbsenceReasonChip.vue";
import InlineCRUDList from "aleksis.core/components/generic/InlineCRUDList.vue";
import DateTimeField from "aleksis.core/components/generic/forms/DateTimeField.vue";
</script>

<template>
  <v-container>
    <inline-c-r-u-d-list
      :headers="headers"
      :i18n-key="i18nKey"
      create-item-i18n-key="kolego.absence.create"
      :gql-query="gqlQuery"
      :gql-create-mutation="gqlCreateMutation"
      :gql-patch-mutation="gqlPatchMutation"
      :gql-delete-mutation="gqlDeleteMutation"
      :default-item="defaultItem"
    >
      <template #datetimeStart="{ item }">
        {{ $d(new Date(item.datetimeStart), "shortDateTime") }}
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #datetimeStart.field="{ attrs, on, item }">
        <div aria-required="true">
          <date-time-field
            v-bind="attrs"
            v-on="on"
            :rules="required"
            :max="item ? item.datetimeEnd : undefined"
            required
          ></date-time-field>
        </div>
      </template>

      <template #datetimeEnd="{ item }">
        {{ $d(new Date(item.datetimeEnd), "shortDateTime") }}
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #datetimeEnd.field="{ attrs, on, item }">
        <div aria-required="true">
          <date-time-field
            v-bind="attrs"
            v-on="on"
            required
            :rules="required"
            :min="item ? item.datetimeStart : undefined"
          ></date-time-field>
        </div>
      </template>

      <template #person="{ item }">
        <v-chip>{{ item.person.fullName }}</v-chip
        >&nbsp;
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #person.field="{ attrs, on }">
        <div aria-required="true">
          <v-autocomplete
            :items="persons"
            item-text="fullName"
            item-value="id"
            v-bind="attrs"
            v-on="on"
            required
            :rules="required"
          />
        </div>
      </template>

      <template #reason="{ item }">
        <absence-reason-chip :absence-reason="item.reason" short />
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #reason.field="{ attrs, on }">
        <div aria-required="true">
          <v-autocomplete
            :items="absenceReasons"
            item-text="shortName"
            item-value="id"
            v-bind="attrs"
            v-on="on"
          />
        </div>
      </template>
    </inline-c-r-u-d-list>
  </v-container>
</template>

<script>
import {
  absences,
  createAbsences,
  deleteAbsences,
  updateAbsences,
} from "./absences.graphql";
import { gqlAbsenceReasons, gqlPersons } from "./helper.graphql";

export default {
  name: "Absences",
  data() {
    return {
      headers: [
        {
          text: this.$t("school_term.date_start"),
          value: "datetimeStart",
        },
        {
          text: this.$t("school_term.date_end"),
          value: "datetimeEnd",
        },
        {
          text: this.$t("person.title"),
          value: "person",
        },
        {
          text: this.$t("kolego.absence.reason"),
          value: "reason",
        },
        {
          text: this.$t("kolego.absence.comment"),
          value: "comment",
        },
      ],
      i18nKey: "kolego.absence",
      gqlQuery: absences,
      gqlCreateMutation: createAbsences,
      gqlPatchMutation: updateAbsences,
      gqlDeleteMutation: deleteAbsences,
      defaultItem: {
        datetimeStart: new Date().toISOString(),
        datetimeEnd: new Date().toISOString(),
        person: "",
        reason: "",
        comment: "",
      },
      required: [(value) => !!value || this.$t("forms.errors.required")],
    };
  },
  apollo: {
    persons: gqlPersons,
    absenceReasons: gqlAbsenceReasons,
  },
};
</script>

<style scoped></style>
