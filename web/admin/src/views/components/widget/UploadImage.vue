<template>
    <div class="flex flex-row flex-wrap">
        <div v-for="(img, i) in fileList">
            <div v-if="img && img.url" class="flex flex-col items-center">
                <ElImage :src="$img(img.url)" :preview-teleported="true" :preview-src-list="[imageUrl]" fit="cover"
                    style="width: 64px; height: 64px;" class="mr-2"></ElImage>
                <ElButton type="danger" @click="handleDelete(i)" link class="!text-xs">删除</ElButton>
            </div>
        </div>

        <ElButton style="width: 64px; height: 64px;" @click="handleUpload">
            <div class="flex flex-col items-center jucstify-center">
                <Icon icon="ant-design:upload-outlined" class="text-2xl mb-1"></Icon>
                <span class="text-8px">上传图片</span>
            </div>
        </ElButton>

    </div>
</template>

<script>
import { request } from '../../../api/request';

export default {
    emits: ['update:modelValue', 'change'],
    props: {
        modelValue: {
            type: String,
            default: ''
        },
        max: {
            type: Number,
            default: 1
        },
        multiple: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            imageUrl: '',
            fileList: []
        }
    },
    watch: {
        modelValue: {
            handler() {
                this.imageUrl = this.$img(this.modelValue)
                if (Array.isArray(this.modelValue)) {
                    this.fileList = this.modelValue.map(item => {
                        if (item.url) return item
                        return {
                            url: item
                        }
                    })
                } else {
                    this.fileList = [{
                        url: this.modelValue
                    }]
                }
            },
            immediate: true
        }
    },
    methods: {
        handleUpload() {
            let input = document.createElement('input')
            input.type = 'file'
            input.accept = 'image/*'
            input.click()
            input.onchange = () => {
                let file = input.files[0]
                request.postForm('/common/upload', {
                    file
                },).then(res => {
                    let url = res.data?.data
                    if (!this.multiple) {
                        this.fileList = [{
                            url
                        }]

                        this.update()
                        return
                    }
                    if (this.fileList.length < this.max) {
                        this.fileList.push({
                            url
                        })

                        this.update()
                    } else {
                        this.$message.warning('最多上传' + this.max + '张图片')
                    }
                })
            }
        },
        handleDelete(i) {
            this.fileList.splice(i, 1)
            this.update()
        },
        update() {
            let urls = this.fileList.map(item => item.url)
            if (!this.multiple) urls = urls[0]
            this.$emit('update:modelValue', urls)
            this.$emit('change', urls)
        }
    },

}

</script>