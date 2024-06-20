<template>
    <div class="p-2">
        <ElCard shadow="never">
            <div class="flex flex-row">
                <div>
                    <h1 class="mb-0 mt-2">{{ meta.table?.title || meta.title }}</h1>
                    <p class="text-gray">{{ meta.description || meta.table.description }}</p>
                </div>
                <div class="flex-grow">
                    <div class="flex flex-row-reverse">

                    </div>
                </div>
            </div>
            <ElDivider class="!mb-4 !mt-2"></ElDivider>
            <Form ref="form" :fields="fields"
            :buttons-container-class-name="currentForm?.buttons_container_class_name || 'w-full'"
            @submitForm="handleSubmitForm"></Form>
        </ElCard>
    </div>
</template>

<script>
import Form from './components/Form.vue'
import { request } from '@/api/request';

export default {
    components: { Form },
    props: {},
    data() {
        return {
            defaultForm: {},
            query:{}
        }
    },
    computed: {
        meta() {
            return this.$route.meta
        },
        currentForm() {
            return this.$route.meta.forms[this.$route.meta.currentForm]
        },
        fields() {
            return this.currentForm?.rows || []
        },
        hasQuery() {
            return Object.keys(this.$route.query).length > 0
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            let detail_param_keys = this.currentForm?.detail_param_keys || []
            let params = {}
            console.log(detail_param_keys, this.$route.query)
            for (let key of detail_param_keys) {
                params[key] = this.$route.query[key]
            }
            this.query = params
            let api = this.currentForm?.detail_api
            if (api && this.hasQuery) {
                request.get(api, {
                    params
                }).then(res => {
                    console.log(res)
                    this.$refs.form.setValues(res.data.data)
                })
            }
        },
        handleSubmitForm(e) {
            let api = this.currentForm?.create_api
            if (this.hasQuery) api = this.currentForm?.update_api
            if (api) {
                request.post(api, e).then(res => {
                    console.log(res)
                    this.$message.success('操作成功')
                    this.$router.go(-1)
                })
            }
        }
    }
}
</script>