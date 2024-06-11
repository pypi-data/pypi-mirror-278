<template>
  <v-data-iterator
    v-bind="$attrs"
    v-on="$listeners"
    :items="items"
    :items-per-page="itemsPerPage"
    :loading="loading"
    :class="elevated ? 'elevation-2' : ''"
    :search="search"
    :custom-filter="deepSearch"
    :sort-by.sync="sortBy"
    :sort-desc.sync="sortDesc"
    multi-sort
    @update:sort-by="handleSortChange"
    @update:sort-desc="handleSortChange"
    :show-select="showSelect"
    selectable-key="selectable"
    @toggle-select-all="handleToggleAll"
  >
    <!-- Bar template -->
    <template #header>
      <c-r-u-d-bar
        :class="{
          'c-r-u-d-iterator-fixed-header': fixedHeader,
          'pa-3': fixedHeader,
        }"
        :flat="!fixedHeader"
        v-bind="$attrs"
        v-on="$listeners"
        @mode="$emit('mode', $event)"
        @loading="handleLoading"
        @items="handleItems"
        @lastQuery="$emit('lastQuery', $event)"
        @search="search = $event"
        @selectable="showSelect = true"
        :selection="selection"
        @selection="handleSelection"
        @deletable="$emit('deletable', $event)"
      >
        <template #filters="{ attrs, on }">
          <slot name="filters" :attrs="attrs" :on="on" />
        </template>

        <template
          v-for="header in computedHeaders"
          #[fieldSlot(header)]="{ item, isCreate, on, attrs }"
        >
          <slot
            :name="fieldSlot(header)"
            :attrs="attrs"
            :on="on"
            :item="item"
            :is-create="isCreate"
          />
        </template>
        <template #additionalActions="{ attrs, on }">
          <slot name="additionalActions" :attrs="attrs" :on="on" />
        </template>
      </c-r-u-d-bar>
      <div
        v-if="fixedHeader"
        class="c-r-u-d-iterator-fixed-header-placeholder"
      />
    </template>

    <template #default="slotProps">
      <slot name="default" v-bind="slotProps" />
    </template>
    <template #loading>
      <slot name="loading"></slot>
    </template>
    <template #no-data>
      <slot name="no-data"></slot>
    </template>
    <template #no-results>
      <slot name="no-results"></slot>
    </template>
  </v-data-iterator>
</template>

<script>
import CRUDBar from "./CRUDBar.vue";

import deepSearchMixin from "../../mixins/deepSearchMixin";
import loadingMixin from "../../mixins/loadingMixin.js";
import syncSortMixin from "../../mixins/syncSortMixin.js";

// TODO: props, data & methods are a subset of CRUDList's -> share?

export default {
  name: "CRUDIterator",
  components: {
    CRUDBar,
  },
  mixins: [deepSearchMixin, loadingMixin, syncSortMixin],
  props: {
    // fixed-header behaves the same as in v-data-table where it is included by vuetify
    /**
     * Fix header to top
     */
    fixedHeader: {
      type: Boolean,
      required: false,
      default: false,
    },
    /**
     * Elevate the iterator?
     * @values true, false
     */
    elevated: {
      type: Boolean,
      required: false,
      default: true,
    },
    /**
     * Number of items shown per page
     * @values natural number
     */
    itemsPerPage: {
      type: Number,
      required: false,
      default: 15,
    },
  },
  emits: ["mode", "lastQuery", "deletable", "items", "selection"],
  data() {
    return {
      items: [],
      // Search
      search: "",
      // Item selection
      showSelect: false,
      selection: [],
      allSelected: false,
    };
  },
  computed: {
    computedHeaders() {
      return "headers" in this.$attrs
        ? this.$attrs.headers.filter((header) => !header.disableEdit)
        : [];
    },
    fixedHeaderTop() {
      return `${this.$vuetify.application.top}px`;
    },
    fixedHeaderWidth() {
      return `calc(100vw - ${this.$vuetify.application.left}px - ${this.$vuetify.application.right}px)`;
    },
    fixedHeaderLeft() {
      return `${this.$vuetify.application.left}px`;
    },
  },
  methods: {
    handleItems(items) {
      this.items = items;
      // Pass on; documented in queryMixin.
      this.$emit("items", items);
    },
    handleSelection(selection) {
      this.selection = selection;
      // Pass on; documented in CRUDBar.
      this.$emit("selection", selection);
    },
    // Item selection
    handleToggleAll({ items, value }) {
      if (value) {
        // There is a bug in vuetify: items contains all elements, even those that aren't selectable
        this.handleSelection(items.filter((item) => item.selectable));
      } else {
        this.handleSelection([]);
      }
      this.allSelected = value;
    },
    // Template names
    fieldSlot(header) {
      return header.value + ".field";
    },
  },
};
</script>

<style lang="scss">
.c-r-u-d-iterator-fixed-header {
  position: fixed;
  width: v-bind(fixedHeaderWidth);
  left: v-bind(fixedHeaderLeft);
  top: v-bind(fixedHeaderTop);
  z-index: 3;
}

.c-r-u-d-iterator-fixed-header-placeholder {
  height: v-bind(fixedHeaderTop);
  position: sticky;
  top: v-bind(fixedHeaderTop);
  z-index: 2;
}
</style>
