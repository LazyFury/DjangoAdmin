<template>
    <div class="flex flex-row relative">
        <div class="light:bg-white dark:bg-dark sub-menu" style="height:calc(100vh - var(--header-bar-height));position: relative;overflow-y: auto;">
            <Menu class="w-180px" :menus="subMenuStore.menus" :is-sub-menu="true"></Menu>
        </div>
        <div style="flex:1;width:100%;height: calc(100vh - var(--header-bar-height));overflow-y: auto;">
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

<style lang="scss" scoped>
    .sub-menu{
        animation: fade-in 0.1s;
    }

    @keyframes fade-in {
        0% {
            opacity: .5;
            transform: translateX(-50%);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }
</style>