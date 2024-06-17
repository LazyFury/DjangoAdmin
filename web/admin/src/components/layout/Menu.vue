<template>
  <div>
    <el-menu
      class="text-xl menus"
      @open="handleOpen"
      @close="handleClose"
      :default-active="defaultActive"
    >
      <template v-for="(item, index) in menus">
        <MenuItem
          v-if="!isSubMenu || !item.children || item.children.length <= 0"
          :item="item"
          @jump="to"
        ></MenuItem>
        <SubMenu
          v-if="item.children && item.children.length > 0 && isSubMenu"
          :item="item"
          @jump="to"
        ></SubMenu>
      </template>
    </el-menu>
  </div>
</template>
<script>
import router from "@/router";
import MenuItem from "./MenuItem.vue";
import SubMenu from "./SubMenu.vue";
import { useSubMenuStore } from "@/pinia/subMenu";
export default {
  components: {
    MenuItem,
    SubMenu,
  },
  props: {
    isSubMenu: {
      type: Boolean,
      default: false,
    },
    menus: {
      type: Array,
      default: () => [
        {
          title: "数据汇总",
          icon: "ant-design:dashboard-outlined",
          path: "/",
          key: "overview",
        },
        {
          title: "用户管理",
          icon: "iconoir:user-circle",
          children: [
            {
              title: "item one",
              path: "/about",
              key: "itemone",
            },
            {
              title: "item two",
              path: "/about1",
              key: "itemtwo",
            },
          ],
        },
        {
          title: "关于 EVA Admin",
          icon: "iconoir:info-circle",
          path: "/about",
          key: "about",
        },
      ],
    },
  },
  data() {
    return {
      defaultActive: "",
    };
  },
  setup() {
    const subMenuStore = useSubMenuStore();
    return {
      subMenuStore,
    };
  },
  watch: {
    currentMenu: {
      handler(val) {
        console.log("currentMenu", val);
        if (!this.isSubMenu && val && val.children) {
          console.log("setSubMenu", val.children);
          this.subMenuStore.setSubMenu(val.children);
        }
      },
      immediate: true,
      deep: true,
    },
  },
  computed: {
    currentMenu() {
      return this.menus.find((el) => el.key === this.defaultActive);
    },
  },
  methods: {
    to(item) {
      if (!this.isSubMenu) {
        this.subMenuStore.setSubMenu(item.children);
      }
      this.$router.push(item.path);
    },
    handleClose() {},
    handleOpen() {},
    findDefaultActive() {
      let href = window.location.href;
      // path = hash last
      let path = href.split("#").pop();
      // remove query
      path = path.split("?")[0];
      // path with out start /
      path = path.replace(/^\//, "");

      // last path
      if (this.isSubMenu) path = path.split("/").pop();
      if (!this.isSubMenu) path = path.split("/")[0];
      console.log(path);
      if (path) this.defaultActive = path;
    },
  },
  created() {},
  mounted() {
    this.findDefaultActive();

    router.afterEach((to, from) => {
      this.findDefaultActive();
    });
  },
};
</script>
<style lang="scss" scoped>
.menus {
  .iconify {
    font-size: 16px !important;
  }
}
</style>
