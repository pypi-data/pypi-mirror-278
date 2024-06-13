<script setup>
import ColorField from "aleksis.core/components/generic/forms/ColorField.vue";
import InlineCRUDList from "aleksis.core/components/generic/InlineCRUDList.vue";
</script>

<template>
  <v-container>
    <inline-c-r-u-d-list
      :headers="headers"
      :i18n-key="i18nKey"
      create-item-i18n-key="kolego.absence_reason.create"
      :gql-query="gqlQuery"
      :gql-create-mutation="gqlCreateMutation"
      :gql-patch-mutation="gqlPatchMutation"
      :gql-delete-mutation="gqlDeleteMutation"
      :default-item="defaultItem"
    >
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #name.field="{ attrs, on }">
        <div aria-required="true">
          <v-text-field
            v-bind="attrs"
            v-on="on"
            :rules="$rules().required.build()"
          />
        </div>
      </template>

      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #shortName.field="{ attrs, on }">
        <div aria-required="true">
          <v-text-field
            v-bind="attrs"
            v-on="on"
            :rules="$rules().required.build()"
          />
        </div>
      </template>

      <template #colour="{ item }">
        <v-chip :color="item.colour" outlined v-if="item.colour">
          {{ item.colour }}
        </v-chip>
        <span v-else>–</span>
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #colour.field="{ attrs, on }">
        <color-field v-bind="attrs" v-on="on" />
      </template>

      <template #default="{ item }">
        <v-switch
          :input-value="item.default"
          disabled
          inset
          :false-value="false"
          :true-value="true"
        />
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #default.field="{ attrs, on }">
        <v-switch
          v-bind="attrs"
          v-on="on"
          inset
          :false-value="false"
          :true-value="true"
          :hint="$t('kolego.absence_reason.default_helptext')"
          persistent-hint
        />
      </template>
    </inline-c-r-u-d-list>
  </v-container>
</template>

<script>
import formRulesMixin from "aleksis.core/mixins/formRulesMixin.js";
import {
  absenceReasons,
  createAbsenceReasons,
  deleteAbsenceReasons,
  updateAbsenceReasons,
} from "./absenceReasons.graphql";

export default {
  name: "AbsenceReasons",
  mixins: [formRulesMixin],
  data() {
    return {
      headers: [
        {
          text: this.$t("kolego.absence_reason.short_name"),
          value: "shortName",
        },
        {
          text: this.$t("kolego.absence_reason.name"),
          value: "name",
        },
        {
          text: this.$t("kolego.absence_reason.colour"),
          value: "colour",
        },
        {
          text: this.$t("kolego.absence_reason.default"),
          value: "default",
        },
      ],
      i18nKey: "kolego.absence_reason",
      gqlQuery: absenceReasons,
      gqlCreateMutation: createAbsenceReasons,
      gqlPatchMutation: updateAbsenceReasons,
      gqlDeleteMutation: deleteAbsenceReasons,
      defaultItem: {
        shortName: "",
        name: "",
        colour: "",
        default: false,
      },
      required: [(value) => !!value || this.$t("forms.errors.required")],
    };
  },
};
</script>

<style scoped></style>
