<template>
    <div class="flex flex-row gap-2">
        <Menu class="w-180px" :menus="subMenuStore.menus" :is-sub-menu="true"></Menu>
        <RouterView :key="$route.meta.key"></RouterView>
    </div>
</template>

<script>
import Menu from '@/components/layout/Menu.vue'
import { useSubMenuStore } from '@/pinia/subMenu'
export default {
    components: {
        Menu
    },
    data() {
        return {
        }
    },
    setup() {
        const subMenuStore = useSubMenuStore()
        return {
            subMenuStore
        }
    }
}
</script>

<style lang="scss" scoped></style>