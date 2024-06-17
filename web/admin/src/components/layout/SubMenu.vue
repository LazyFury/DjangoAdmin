<template>
    <div>
        <el-sub-menu v-if="item.children && item.children.length > 0" :key="item.key" :index="item.key">
            <template #title>
                <Icon :icon="item.icon"></Icon>
                <span class="ml-1">{{ $t(item.title) }}</span>
            </template>
            <div v-for="(childItem) in item.children">
                <MenuItem v-if="!childItem.children || childItem.children.length<=0" :item="childItem" @jump="e=>$emit('jump',e)"></MenuItem>
                <div v-if="childItem.children && childItem.children.length>0" >
                    <sub-menu :item="childItem" ></sub-menu>
                </div>
            </div>
        </el-sub-menu>
    </div>
</template>

<script>
import MenuItem from './MenuItem.vue'
export default {
    name: "sub-menu",
    components:{
        MenuItem
    },
    props: {
        item: {
            type: Object,
            default: () => ({})
        }
    },
    methods: {
        to(path) {
            this.$router.push(path)
        }
    }
}
</script>

<style lang="scss" scoped></style>