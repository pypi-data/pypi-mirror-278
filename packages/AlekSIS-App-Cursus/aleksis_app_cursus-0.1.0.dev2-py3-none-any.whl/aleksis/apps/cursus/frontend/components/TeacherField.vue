<script setup>
import SubjectChip from "./SubjectChip.vue";
</script>

<template>
  <v-autocomplete
    v-bind="$attrs"
    v-on="$listeners"
    multiple
    :items="teacherList"
    item-text="fullName"
    item-value="id"
    :loading="$apollo.queries.persons.loading"
  >
    <template #item="data">
      <v-list-item-action>
        <v-checkbox v-model="data.attrs.inputValue" />
      </v-list-item-action>
      <v-list-item-content>
        <v-list-item-title>{{ data.item.fullName }}</v-list-item-title>
        <v-list-item-subtitle v-if="data.item.shortName"
          >{{ data.item.shortName }}
        </v-list-item-subtitle>
        <v-list-item-subtitle
          v-if="showSubjects && data.item.subjectsAsTeacher.length"
        >
          <subject-chip
            v-for="subject in data.item.subjectsAsTeacher"
            :key="subject.id"
            :subject="subject"
            :prepend-icon="subject.id === prioritySubject.id ? '$success' : ''"
            :short-name="true"
            x-small
            class="mr-1"
          />
        </v-list-item-subtitle>
      </v-list-item-content>
    </template>
    <template #prepend-inner>
      <slot name="prepend-inner" />
    </template>
    <template #selection="data">
      <slot name="selection" v-bind="data" />
    </template>
  </v-autocomplete>
</template>

<script>
import { gqlTeachers } from "./helper.graphql";

export default {
  name: "TeacherField",
  data() {
    return {
      persons: [],
    };
  },
  props: {
    showSubjects: {
      type: Boolean,
      required: false,
      default: false,
    },
    prioritySubject: {
      type: Object,
      required: false,
      default: null,
    },
  },
  computed: {
    teacherList() {
      if (this.prioritySubject) {
        let matching = [];
        let nonMatching = [];

        this.persons.forEach((p) => {
          if (
            p.subjectsAsTeacher.some((s) => s.id === this.prioritySubject.id)
          ) {
            matching.push(p);
          } else {
            nonMatching.push(p);
          }
        });

        return matching.concat(nonMatching);
      } else {
        return this.persons;
      }
    },
  },
  apollo: {
    persons: {
      query: gqlTeachers,
    },
  },
};
</script>

<style scoped></style>
