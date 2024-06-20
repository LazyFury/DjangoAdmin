<template>
    <div>
        <!-- {{ form }} -->
        <ElForm ref="formRef" @submit.prevent.stop="() => { }" :inline="false" :model="form" :rules="rules"
            :label-width="120" class="mt-0">
            <div class="mb-4 grid xl:grid-cols-2">
                <div v-for="field in fields" v-if="!multiRowMode">
                    <span>not support yet!</span>
                </div>
            </div>


            <div v-if="multiRowMode" v-for="items in fields" class="flex flex-row flex-wrap">
                <div class="w-line mb-2"></div>
                <template v-for="field in items" :key="field.prop">
                    <ElFormItem v-if="!field.hidden" :label="field.label + ':'" :prop="field.prop" :style="{
                        width: field.width
                    }">
                        <slot :name="field.prop" :fields="fields" :field="field" :form="form">
                            <FormItem :field="field" :key="field.prop" v-model="form[field.prop]"></FormItem>
                        </slot>
                    </ElFormItem>
                </template>
            </div>

            <ElDivider class="!my-4" />

            <ElFormItem label=" ">
                <div class="" :class="buttonsContainerClassName">
                    <ElButton @click="handleSubmit()" type="primary" class="w-24">保存</ElButton>
                </div>
            </ElFormItem>

        </ElForm>


    </div>
</template>
<script>
import FormItem from './FormItem.vue'
export default {
    components: { FormItem },
    props: {
        fields: {
            type: Array,
            default: () => []
        },
        title: {
            type: String,
            default: ''
        },
        defaultForm: {
            type: Object,
            default: () => ({})
        },
        progressFormData: {
            type: Function,
            default: (res) => res
        },
        buttonsContainerClassName: {
            type: String,
            default: 'flex flex-row items-center justify-end'
        }
    },
    computed: {
        rules() {
            // check required in fields 
            let map = {}
            this.flatFields.forEach(el => {
                if (el.required) {
                    map[el.prop] = [
                        { required: true, message: el.message || el.placeholder, trigger: 'blur' }
                    ]
                }
            })
            return map;
        },
        flatFields() {
            if (!this.multiRowMode) return this.fields;
            return this.fields.reduce((acc, cur) => {
                return acc.concat(cur)
            }, [])
        },
        multiRowMode() {
            return this.fields && this.fields[0] && Array.isArray(this.fields[0])
        },
        isAdd() {
            return !this.form.id
        },
        formTitle() {
            return this.isAdd ? '新增' : '编辑'
        }
    },
    data() {
        return {
            form: {

            }
        };
    },
    watch: {

    },
    methods: {
        handleSubmit() {
            this.$refs.formRef.validate((valid) => {
                if (valid) {
                    this.$emit('submitForm', this.form)
                }
            })
        },
        edit(data) {
            this.reset()
            let form = JSON.parse(JSON.stringify(data))
            if (this.progressFormData && typeof this.progressFormData === 'function') {
                form = this.progressFormData(form)
            }
            this.setDefaultValues()
            this.form = Object.assign(this.form, form)
            this.$forceUpdate()
        },
        setValues(data) {
            this.edit(data)
        },
        setDefaultValues() {
            this.flatFields.forEach(el => {
                this.form[el.prop] = el.defaultValue
            })
        },
        close() {
            this.reset()
        },
        reset() {
            this.$refs.formRef.resetFields()
            let form = JSON.parse(JSON.stringify(this.defaultForm))
            this.form = form
        }
    },
    created() { },
    mounted() { }
};
</script>
<style lang="scss" scoped></style>