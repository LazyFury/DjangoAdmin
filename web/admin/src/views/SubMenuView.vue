<template>
    <div class="flex flex-row gap-2">
        <div class=" min-h-90vh light:bg-white dark:bg-dark border-solid border-1px rounded-4px overflow-hidden light:border-color-gray-200">
            <Menu class="w-180px" :menus="subMenuStore.menus" :is-sub-menu="true"></Menu>
        </div>
        <div style="flex:1;width:100%">
            <RouterView :key="$route.meta.key"></RouterView>
        </div>
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