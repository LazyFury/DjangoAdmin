<template>
	<view :style="attrs.style" :class="attrs.class">
		<slot></slot>
	</view>
</template>

<script>
	export default {
		props:{
			attrs:{
				type:Object,
				default:()=>({})
			}
		}
	}
</script>

<style>
</style>