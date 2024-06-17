import { defineStore } from 'pinia'

export const useSubMenuStore = defineStore('subMenu', {
    state: () => {
        return {
            menus: []
        }
    },
    getters: {
        hasSubMenu: (state) => state.menus && state.menus.length > 0
    },
    actions: {
        setSubMenu(menus: any) {
            this.menus = menus
        }
    }
})