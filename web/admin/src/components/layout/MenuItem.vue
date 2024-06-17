<template>
  <div>
    <el-menu-item
      v-if="item.type == 'gap'"
      :disabled="true"
      :index="item.key"
      @click="to(item)"
    >
      <Icon :icon="item.icon"></Icon>
      <span class="ml-1">{{ $t(item.title) }}</span>
    </el-menu-item>
    <el-menu-item v-else :index="item.key" @click="to(item)">
      <Icon :icon="item.icon"></Icon>
      <span class="ml-1">{{ $t(item.title) }}</span>
    </el-menu-item>
  </div>
</template>

<script>
export default {
  components: {},
  props: {
    item: {
      type: Object,
      default: () => ({}),
    },
  },
  methods: {
    to(item) {
      this.$emit("jump", item);
    },
  },
};
</script>

<style lang="scss" scoped></style>
