<template>
	<view class="status-bar"></view>
	<uni-nav-bar title="Home" :shadow="false" :border="false"></uni-nav-bar>
	<view class="content">
		<template v-for="(component, index) in layouts" :key="index">
			<render :component="component" />
		</template>
	</view>
</template>

<script>
import render from '@/components/design/render';

import icon from '@/static/logo.png';

const flex = {
	display: 'flex',
	'flex-direction': 'column',
	'align-items': 'center',
	'justify-content': 'center',
}

const menuStyle = {
	display: 'flex',
	'flex-direction': 'column',
	'align-items': 'center',
	'justify-content': 'center',
	background: '#fdfdfd',
	'margin-right': '4rpx',
	'margin-bottom': '4rpx',
	height: '180rpx',
	width: 'calc((750rpx - 12px) / 4)'
};

const menuImage = {
	name: 'image',
	src: icon,
	attrs: {
		style: {
			width: '96rpx',
			height: '96rpx',
			background: '#ddd'
		}
	}
};
export default {
	components: { render },
	data() {
		return {
			title: 'Hello',
			layouts: [
				{
					name:"notice",
					attrs:{
						text:"hello world!",
						showIcon:true
					}
				},
				{
					name: 'swiper',
					attrs: {
						'indicator-active-color': 'white',
						style: {
							height: '400rpx'
						}
					},
					item: {
						attrs: {
							style: {
								padding: '20rpx',
								background: '#ddd',
								height: '400rpx'
							}
						}
					},
					children: [
						{
							name: 'text',
							content: 'swiper item 1'
						}
					]
				},
				{
					name: 'spacer',
					attrs: {
						style: {
							height: '20rpx'
						}
					}
				},
				{
					name: 'spacer',
					attrs: {
						style: {
							height: '20rpx'
						}
					}
				},
				{
					name: 'view',
					attrs: {
						style: {
							display: 'flex',
							'flex-direction': 'row',
							'flex-wrap': 'wrap',
							'padding-left': '4rpx'
						}
					},
					api: {
						url: '/api/getMenus',
						dataKey: 'res.data',
						dataName: 'menus',
						onclick: {
							func: '$push',
							args: ['/pages/product/detail']
						}
					},
					children: [
						{
							name: 'view',
							attrs: {
								style: {
									...menuStyle
								}
							},
							children: [menuImage, { name: 'text', content: 'menu' }]
						},
						{
							name: 'view',
							attrs: {
								style: {
									...menuStyle
								}
							},
							children: [
								{
									name: 'badge',
									attrs:{
										text: '999',
										absolute:"rightTop",
										size:"large",
										'custom-style':{
											
										}
									},
									children:[
										{
											name:"view",
											attrs:{
												style:{
													...flex
												}
											},
											children:[
												menuImage,
												{ name: 'text', content: 'menu' }
											]
										}
									]
								},
							]
						},
						{
							name: 'view',
							attrs: {
								style: {
									...menuStyle
								}
							},
							children: [menuImage, { name: 'text', content: 'menu' }]
						},
						{
							name: 'view',
							attrs: {
								style: {
									...menuStyle
								}
							},
							children: [menuImage, { name: 'text', content: 'menu' }]
						},
						{
							name: 'view',
							attrs: {
								style: {
									...menuStyle
								}
							},
							children: [menuImage, { name: 'text', content: 'menu' }]
						},
						{
							name: 'view',
							attrs: {
								style: {
									...menuStyle
								}
							},
							children: [menuImage, { name: 'text', content: 'menu' }]
						}
					]
				},
				
			]
		};
	},
	onLoad() {},
	methods: {}
};
</script>

<style style="scss" scope>
.status-bar {
	height: calc(0px + env(safe-area-inset-top));
}
</style>
