/**
 * Mixin to provide common fields for all components specific to a singular documentation inside the coursebook
 */
export default {
  props: {
    /**
     * The documentation in question
     */
    documentation: {
      type: Object,
      required: true,
    },
    /**
     * The query used by the coursebook. Used to update the store when data changes.
     */
    affectedQuery: {
      type: Object,
      required: true,
    },
    /**
     * Whether the documentation is currently in the compact mode (meaning coursebook row)
     */
    compact: {
      type: Boolean,
      required: false,
      default: false,
    },
    /**
     * Activator attributes and event listeners to open documentation dialog in different places
     */
    dialogActivator: {
      type: Object,
      required: false,
      default: () => ({ attrs: {}, on: {} }),
    },
  },

  computed: {
    /**
     * All necessary props bundled together to easily pass to child components
     * @returns {{compact: Boolean, documentation: Object, dialogActivator: Object<{attrs: Object, on: Object}>}}
     */
    documentationPartProps() {
      return {
        documentation: this.documentation,
        compact: this.compact,
        dialogActivator: this.dialogActivator,
        affectedQuery: this.affectedQuery,
      };
    },
  },
};
