/**
 * This mixin provides shared props for each person overview card.
 */
export default {
  props: {
    /**
     * The person for the current person overview
     */
    person: {
      type: Object,
      required: true,
    },
    /**
     * The optional school term for the current person overview
     */
    schoolTerm: {
      type: Object,
      required: false,
      default: null,
    },
  },
};
