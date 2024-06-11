<script>
export default {
  name: "SubjectChip",
  extends: "v-chip",
  props: {
    subject: {
      type: Object,
      required: true,
    },
    shortName: {
      type: Boolean,
      required: false,
      default: false,
    },
    prependIcon: {
      type: String,
      default: null,
      required: false,
    },
    appendIcon: {
      type: String,
      default: null,
      required: false,
    },
  },
};
</script>

<template>
  <v-chip
    v-bind="$attrs"
    v-on="$listeners"
    :color="subject.colourBg"
    :text-color="subject.colourFg"
  >
    <v-icon left v-if="prependIcon">{{ prependIcon }}</v-icon>
    {{ shortName ? subject.shortName : subject.name }}
    <v-icon right v-if="appendIcon">{{ appendIcon }}</v-icon>
  </v-chip>
</template>
