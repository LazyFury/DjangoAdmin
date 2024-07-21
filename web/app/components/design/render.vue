<template>
	<swiper
		v-if="component.name == 'swiper'"
		:style="component.attrs.style"
		:attrs="component.attrs"
		class="swiper"
		:indicator-dots="true"
		:autoplay="true"
		:interval="3000"
		:duration="300"
	>
		<swiper-item v-for="(child, index) in component.children" :key="index">
			<uiview :attrs="component.item && component.item.attrs">
				<render :component="child" />
			</uiview>
		</swiper-item>
	</swiper>

	<uiview v-if="component.name == 'spacer'" style="height: 20rpx" :attrs="component.attrs"></uiview>

	<uiview v-if="component.name == 'text'" :attrs="component.attrs">
		<text>{{ component.content }}</text>
	</uiview>

	<uiview v-if="component.name == 'view'" :attrs="component.attrs">
		<template v-for="child in component.children">
			<render :component="child" />
		</template>
	</uiview>

	<image v-if="component.name == 'image'" :src="component.src" :style="component.attrs.style" mode="aspectFit"></image>

	<uni-badge v-if="component.name == 'badge'" v-bind="component.attrs">
		<template v-for="child in component.children">
			<render :component="child" />
		</template>
	</uni-badge>
	
	<uni-notice-bar v-if="component.name == 'notice'" v-bind="component.attrs"></uni-notice-bar>
</template>

<script>
import uiview from './uiview.vue';
export default {
	name: 'Render',
	components: { uiview },
	props: {
		component: {
			type: Object,
			default: () => ({})
		}
	}
};
</script>

<style></style>
