<template>
    <!-- textarea  -->
    <ElInput @change="handleUpdate" v-model="value" v-if="field.type == 'textarea'" type="textarea"
        :placeholder="field.placeholder" v-bind="field.props"></ElInput>
    <!-- password  -->
    <ElInput @change="handleUpdate" v-model="value" v-if="field.type == 'password'" type="password"
        :placeholder="field.placeholder">
    </ElInput>
    <!-- select  -->
    <div v-if="field.type == 'select'" class="flex flex-row items-center w-full">
        <ElSelect class="w-full" @change="handleUpdate" v-model="value" :placeholder="field.placeholder"
            v-bind="field.props">
            <ElOption v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></ElOption>
        </ElSelect>
        <div class="mr-2"></div>
        <!-- refresh  -->
        <ElButton @click="getOptions" type="text" link>
            <Icon icon="el:refresh" class=""></Icon>
        </ElButton>
    </div>

    <!-- cascader  -->
    <div v-if="field.type == 'cascader'">
        <ElCascader @change="handleUpdate" v-model="value" :options="options" :props="field.props"
            :placeholder="field.placeholder" v-bind="field.props"></ElCascader>
        <ElButton @click="getOptions" type="text" link>
            <Icon icon="el:refresh" class=""></Icon>
        </ElButton>
    </div>
    <!-- switch -->
    <ElSwitch @change="handleUpdate" v-model="value" v-if="field.type == 'switch'" :active-text="field.checkedChildren">
    </ElSwitch>

    <!-- checkbox  group  -->
    <ElCheckboxGroup @change="handleUpdate" v-model="value" v-if="field.type == 'checkbox'">
        <ElCheckbox v-for="item in options" :key="item.value" :label="item.value">{{ item.label }}</ElCheckbox>
    </ElCheckboxGroup>

    <!-- sigle checkbox as bool  -->
    <ElCheckbox @change="handleUpdate" v-model="value" v-if="field.type == 'checkbox-as-bool'">
        {{ field.label }}
    </ElCheckbox>

    <!-- radio  -->
    <ElRadioGroup @change="handleUpdate" v-model="value" v-if="field.type == 'radio'">
        <ElRadio v-for="item in options" :key="item.value" :label="item.value">{{ item.label }}</ElRadio>
    </ElRadioGroup>

    <!-- radio-button  -->
    <ElRadioGroup @change="handleUpdate" v-model="value" v-if="field.type == 'radio-button'">
        <ElRadioButton v-for="item in options" :key="item.value" :label="item.value">{{ item.label }}</ElRadioButton>
    </ElRadioGroup>

    <!-- input  -->
    <ElInput v-model="value" @change="handleUpdate" :type="field.epInputType || 'text'"
        v-if="!field.type || field.type == 'input'" :placeholder="field.placeholder" v-bind="field.props">
        <!-- suffix  -->
        <template v-if="field.suffix" #suffix>
            <div>
                {{ field.suffix }}
            </div>
        </template>
        <!-- prefix -->
        <template v-if="field.prefix" #prefix>
            <div>
                {{ field.prefix }}
            </div>
        </template>
    </ElInput>

    <!-- quill editor  -->
    <div v-if="field.type == 'quill'" v-bind="field.props">
        <QuillEditor v-model="value" @change="handleUpdate"></QuillEditor>
    </div>


    <!-- ！！！Warn:inline 的布局下有对齐的文件，尽量使 formItem 在单独一行 -->
    <div v-if="field.tips" class="text-xs text-gray mt-1">
        <div v-html="field.tips"></div>
    </div>


    <!-- upload image  -->
    <UploadImage v-if="field.type == 'upload-image'" v-model="value" v-bind="field.props"></UploadImage>
</template>
<script>
import { request } from '@/api/request'
import { ElCheckbox } from 'element-plus';
import QuillEditor from '@/components/QuillEditor.vue'
import UploadImage from '@/views/components/widget/UploadImage.vue'


export default {
    components: { ElCheckbox, QuillEditor, UploadImage },
    props: {
        field: {
            type: Object,
            default: () => ({})
        },
        modelValue: {
            type: [String, Number, Array, Object],
            default: () => ''
        }
    },
    data() {
        return {
            options: [],
            value: "",
        };
    },
    watch: {
        modelValue: {
            handler(val) {
                if (this.field.type == 'switch') return this.value = !!val
                this.value = val
            },
            immediate: true
        },
        value: {
            handler(val) {
                this.$emit('update:modelValue', this.progressValue(val))
                this.$emit('change', this.progressValue(val))
            }
        }
    },
    computed: {},
    methods: {
        handleUpdate(val) {
            this.$emit('update:modelValue', this.progressValue(val))
        },
        progressValue(v) {
            // cascader 单选，如果返回数组，取最后一个，要判断是否是数组，否则更新会递归
            if (this.field.type == 'cascader' && !this.field?.props?.multiple && Array.isArray(v)) return v ? v[v.length - 1] : v
            return v
        },
        progressOption(v) {
            let label_name = this.field.props?.label || 'label'
            let backend_label_names = ['name', 'title', 'label', 'username']
            let value_name = this.field.props?.value || 'id'
            let backend_value_names = ['id', 'value']

            let label = ""
            let value = ""

            if (v[label_name]) {
                label = v[label_name]
            }

            if (v[value_name]) {
                value = v[value_name]
            }

            if (!label) {
                for (let i = 0; i < backend_label_names.length; i++) {
                    if (v[backend_label_names[i]]) {
                        label = v[backend_label_names[i]]
                        break
                    }
                }
            }

            if (!value) {
                for (let i = 0; i < backend_value_names.length; i++) {
                    if (v[backend_value_names[i]]) {
                        value = v[backend_value_names[i]]
                        break
                    }
                }
            }


            return {
                label,
                value: value + "",
                children: v.children ? v.children.map(this.progressOption) : []
            }
        },
        getOptions() {
            if (this.field.options) {
                this.options = this.field.options
            } else
                if (this.field.props?.remoteDataApi) {
                    request.get(this.field.props?.remoteDataApi, { params: { page: 1, size: 999 } }).then(res => {
                        let data = res.data?.data?.list || []
                        let options = data.map(this.progressOption)
                        this.options = options
                    })
                }
        }
    },
    created() { },
    mounted() {
        this.getOptions()

        if (this.field.type == 'checkbox') {
            this.value = this.value || []
        }
        if (this.field.type == 'switch') {
            this.value = !!this.value
        }
    }
};
</script>
<style lang="scss" scoped></style>