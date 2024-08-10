<template>
    <div class="p-2">
        <ElCard shadow="never">
            <!-- {{ $route.meta }} -->
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

            <div v-if="filters && filters.rows?.length > 0">
                <div>
                    <ElForm :inline="true" :model="searchForm" @submit.prevent.native="e => { }" class="mb-0">
                        <div v-for="fields in filters.rows">
                            <ElFormItem v-for="field in fields" :key="field.prop" :label="field.label"
                                :prop="field.prop" :class="[]" :style="{ 'min-width': field.width || '100px' }">
                                <FormItem :field="field" v-model="searchForm[field.prop]" @change="load()"></FormItem>
                            </ElFormItem>
                        </div>
                    </ElForm>
                </div>
                <ElDivider class="!mb-4 !mt-0"></ElDivider>
            </div>

            <div v-if="searchFormFields && searchFormFields.length > 0">
                <ElForm :inline="true" :model="searchForm" @submit.prevent.native="e => { }" class="mb-0">
                    <div v-for="fields in searchFormFields">
                        <ElFormItem v-show="!field.hidden" v-for="field in fields" :key="field.prop"
                            :label="field.label" :prop="field.prop" :class="[]"
                            :style="{ 'min-width': field.width || '100px' }">
                            <FormItem :field="field" v-model="searchForm[field.prop]"></FormItem>
                        </ElFormItem>
                    </div>
                    <ElFormItem>
                        <ElButton type="primary" @click="submitSearch">
                            <Icon icon="heroicons-solid:magnifying-glass" class="mt-0px mr-4px"></Icon>
                            <span>{{ $t("search") }}</span>
                        </ElButton>
                        <!-- reset  -->
                        <ElButton type="default" @click="resetSearchForm">
                            <Icon icon="la:trash-restore-alt" class="mt-0px mr-4px"></Icon>
                            <span>{{ $t("reset") }}</span>
                        </ElButton>
                    </ElFormItem>
                </ElForm>
                <ElDivider class="!mb-4 !mt-0"></ElDivider>
            </div>


            <!-- betch actions  -->
            <div class="mb-4">
                <ElButton :disabled="!canAdd" type="primary" @click="handleCreate()">
                    <Icon icon="ant-design:plus-outlined"></Icon>
                    <span>添加</span>
                </ElButton>
                <ElButton :loading="loading" type="default" @click="load">
                    <Icon v-if="!loading" icon="ant-design:reload-outlined"></Icon>
                    <span>{{ $t("refresh") }}</span>
                </ElButton>

                <!-- divider vertical  -->
                <ElDivider direction="vertical" class="mx-4"></ElDivider>

                <ElButton v-for="action in batchActions" :key="action.key" :loading="loading"
                    :type="action.props?.type || 'default'" @click="handlerTableBatchAction(action)">
                    <Icon :icon="action.icon" />
                    <span>{{ action.label }}</span>
                </ElButton>

                <!-- 导出 -->
                <ElButton type="default" @click="exportData">
                    <Icon icon="ant-design:export-outlined"></Icon>
                    <span>导出</span>
                </ElButton>
            </div>
            <div class="overflow-x-auto" :style="{
                width: `calc(100vw - ${subMenuStore.hasSubMenu ? 362 : 180}px)`
            }">
                <ElTable ref="tableRef" size="default" v-loading="loading" :data="tableData" :border="true" stripe
                    :tree-props="{ hasChildren: 'hasChildren', children: 'children' }" row-key="id"
                    @sort-change="handleSortChange">
                    <!-- selection  -->
                    <ElTableColumn type="selection" width="55"></ElTableColumn>

                    <!-- id  -->
                    <ElTableColumn label="ID" :width="table.expand ? 120 : 80" prop="id"></ElTableColumn>

                    <ElTableColumn v-for="column in columns" :key="column.prop"
                        :sortable="column.sortable ? 'custom' : false" :label="column.label" :width="column.width"
                        v-bind="column.props">
                        <template #default="{ row }" v-if="!column.slot">
                            <div :class="[column.className]" v-if="column.type == 'render'">
                                {{ column.render(row) }}
                            </div>
                            <!-- switch  -->
                            <ElSwitch v-if="column.type == 'switch'" v-model="row[column.prop]" inactive-color="#ff4949"
                                active-text="" inactive-text="" disabled></ElSwitch>
                            <!-- checkbox  -->
                            <ElCheckbox v-if="column.type == 'checkbox'" v-model="row[column.prop]" disabled>
                            </ElCheckbox>

                            <!-- select  -->
                            <ElSelect v-if="column.type == 'select'" v-model="row[column.prop]"
                                :placeholder="column.placeholder" clearable>
                                <ElOption v-for="option in column.options" :key="option.value" :label="option.label"
                                    :value="option.value"></ElOption>
                            </ElSelect>
                            <!-- icon  -->
                            <Icon v-if="column.type == 'icon'" :icon="row[column.prop]" :class="[column.className]">
                            </Icon>
                            <!-- image  -->
                            <ElImage :attrs="column.props" :class="[(column.className || 'w-40px h-40px')]" v-if="column.type == 'image'" :src="$img(row[column.prop])" fit="cover"
                                :preview-teleported="true"
                                :preview-src-list="row[column.prop] ? [$img(row[column.prop])] : []"
                                ></ElImage>
                            <ElTag v-if="column.type == 'tag'" :type="column.props?.type || ''">{{ row[column.prop] }}
                            </ElTag>

                            <!-- tags  -->
                            <div v-if="column.type == 'tags'" class="flex flex-row flex-wrap gap-1">
                                <ElTag v-for="tag in row[column.prop]" :key="tag" :type="column.props?.type || ''">
                                    {{ tag }}
                                </ElTag>
                            </div>

                            <!-- link  -->
                            <ElLink type="primary" v-if="column.type == 'link'" :underline="false"
                                :href="makeUrl(row, column, column.props?.url_id || column.prop)"
                                :target="column.props?.url_target || '_self'">
                                {{ column.prefix }}{{ row[column.prop] }}{{ column.suffix }}
                            </ElLink>
                        </template>
                        <template v-if="column.slot" #default="{ row }">
                            <slot :name="column.slot" :row="row"></slot>
                        </template>
                    </ElTableColumn>

                    <!-- actions  -->
                    <ElTableColumn fixed="right" v-if="actions?.length" label="操作" min-width="150px">
                        <template #default="{ row }">
                            <ElButton v-for="action in actions" link :key="action.key"
                                :type="action.props?.type || 'primary'" @click="handlerRowAction(row, action)">
                                <Icon :icon="action.icon" />
                                <span>{{ action.label }}</span>
                            </ElButton>
                        </template>
                    </ElTableColumn>
                </ElTable>
            </div>
            <!-- pagination  -->
            <div class="flex mt-2">
                <ElPagination small layout="total,sizes, prev, pager, next, jumper" background
                    :hide-on-single-page="false" v-model:current-page="pagination.currentPage"
                    v-model:page-size="pagination.pageSize" :page-sizes="[5, 10, 20, 50, 100]" :total="pagination.total"
                    @current-change="handleCurrentPageChange" @size-change="handlePageSizeChange"></ElPagination>
            </div>
        </ElCard>

        <slot v-for="form in formsList" :name="form.prop">
            <ElDialog :title="form.title" :class="form.prop" v-model="isFormsActiveMapping[form.prop]"
                class="!md:w-640px !w-full !lg:w-960px">
                <Form :key="$route.meta.key + '-form-' + form.prop" :ref="form.prop" :title="form.title"
                    :fields="form.rows" @submitForm="e => handleFormSubmit(e, form)">
                </Form>
            </ElDialog>
        </slot>
    </div>
</template>
<script>
import { ElButton, ElPagination } from 'element-plus';
import { request } from '@/api/request';
import Form from '@/views/components/Form.vue'
import FormItem from './components/FormItem.vue';
import config from '@/config';
import { useSubMenuStore } from '../pinia/subMenu';
export default {
    components: { ElPagination, Form, FormItem },
    props: {},
    data() {
        return {
            meta: this.$route.meta,
            searchForm: {},
            pagination: {
                currentPage: 1,
                pageSize: this.$route.meta?.table?.pageSize || 10,
                total: 0
            },
            tableData: [],
            loading: false,
            editModal: false,

            isFormsActiveMapping: {},
            fromActionsMapping: {}
        };
    },
    setup() {
        const subMenuStore = useSubMenuStore()
        return {
            subMenuStore
        }
    },
    watch: {},
    computed: {
        api() {
            return this.meta.api
        },
        table() {
            return this.meta.table || {}
        },
        searchFormFields() {
            return this.meta.table?.search?.rows || []
        },
        filters() {
            return this.meta.table?.filters || []
        },
        forms() {
            return this.meta.forms || []
        },
        formsList() {
            return Object.keys(this.forms).map(key => ({
                prop: key,
                ...this.forms[key]
            }))
        },
        addForm() {
            return this.meta.forms?.create || { rows: [] }
        },
        canAdd() {
            return this.addForm && this.addForm.rows?.length > 0
        },
        columns() {
            console.log(this.meta)
            let columns = this.meta.table?.columns || this.meta.columns || []
            if (typeof columns === 'string') {
                columns = JSON.parse(columns)
            }
            if (typeof columns === 'string') {
                return
            }
            console.log(columns)
            columns = columns?.map(v => ({
                ...v,
                dataIndex: v.dataIndex ? v.dataIndex : 999
            })).sort((a, b) => a.dataIndex - b.dataIndex) || []
            return (columns || []).map(column => {
                return {
                    ...column,
                    type: column.type || 'render',
                    render: (row) => {
                        column.key = column.prop;
                        if (column.slot) return ""
                        if (column.type === '' || column.type === 'render') {
                            let { valueType: type, key, mapping_key, data = [], def, formatStr = "", prefix = "", suffix = "" } = column || {}
                            let formatConfig = column.formatter
                            if (type === 'mapping') {
                                console.log(data)
                                console.log(row[column.key])
                                return data.find(item => item[key] == row[column.key])?.[mapping_key] || def || ""
                            }

                            if (type === 'date') {
                                return row[column.key] ? this.$dayjs(row[column.key]).format('YYYY-MM-DD HH:mm:ss') : ''
                            }

                            if (type === 'datetime') {
                                return row[column.key] ? this.$dayjs(row[column.key]).format('YYYY-MM-DD HH:mm:ss') : ''
                            }
                            // number 
                            if (type === 'number') {
                                let result = row[column.key] ? this.$numeral(row[column.key]).format(formatStr || '0,0.00') : ''
                                return `${prefix}${result}${suffix}`
                            }

                            // bool 
                            if (type === 'boolean') {
                                return row[column.key] ? (formatConfig.trueText || '是') : (formatConfig.falseText || '否')
                            }
                        }
                        return row[column.key]
                    }
                }
            })
        },
        actions() {
            return (this.meta.table?.actions || [
                {
                    key: 'edit',
                    title: '编辑',
                    props: {
                        type: 'primary'
                    },
                    form_key: 'edit_form',
                    type: 'form'
                },
                {
                    key: 'delete',
                    title: '删除',
                    props: {
                        type: 'danger'
                    },
                    type: 'api',
                    api_key: 'delete'
                }
            ])
        },
        batchActions() {
            return this.meta.table?.batch_actions || []
        }
    },
    methods: {
        handlerTableBatchAction(action) {
            let rows = this.getTableSelection()
            if (rows.length == 0) {
                return this.$message.error('请选择数据')
            }
            if (action.confirm) {
                this.$confirm(action.confirm.message, action.confirm.title, {
                    confirmButtonText: action.confirm.confirmButtonText || '确定',
                    cancelButtonText: action.confirm.cancelButtonText || '取消',
                    type: action.confirm.type || 'warning'
                }).then(() => {
                    this.handleTableBatchActionApi(rows, action)
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消'
                    });
                });
                return
            } else {
                this.handleTableBatchActionApi(rows, action)
            }
        },
        handleTableBatchActionApi(rows, action) {
            let { api_key, param_keys, row_key, ids_name = "ids" } = action
            if (api_key) {
                let params = {}
                if (row_key) {
                    params[ids_name] = rows.map(row => row[row_key])
                }
                let url = this.api[api_key]
                if (!url) throw new Error('api_key not found')
                request.post(url, params).then(res => {
                    if (res.data?.code == 200) {
                        this.load()
                    }
                })
            }
        },
        handleCreate() {
            if(this.meta?.table.add_btn){
                return this.handlerRowAction({}, this.meta?.table.add_btn)
            }
            this.handleRowActionForm({}, {
                form_key: 'create',
                type: 'form',
                api_key: 'create'
            })
        },
        handlerRowAction(row, action) {

            const exec = (action) => {
                if (action.type == 'api') {
                    return this.handleRowActionApi(row, action)
                }
                if (action.type == 'form') {
                    return this.handleRowActionForm(row, action)
                }
                if (action.type == 'router') {
                    let param_keys = action?.param_keys // [{k:v}]
                    let query = {}
                    if (param_keys) {
                        for (let item of param_keys) {
                            let [k,] = Object.keys(item)
                            let v = row[item[k]]
                            query[k] = v
                        }
                    }
                    console.log(query, param_keys)
                    return this.$router.push({
                        path: action.path,
                        query
                    })
                }
            }

            if (action.confirm) {
                this.$confirm(action.confirm.message, action.confirm.title, {
                    confirmButtonText: action.confirm.confirmButtonText || '确定',
                    cancelButtonText: action.confirm.cancelButtonText || '取消',
                    type: action.confirm.type || 'warning'
                }).then(() => {
                    exec(action)
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消'
                    });
                });
                return
            } else {
                exec(action)
            }
        },
        handleRowActionForm(row, action) {
            // console.log(this.$refs, action)
            let { form_key } = action
            let keys = form_key.split("|")
            let current_key;
            let form
            let formRef

            for (let key of keys) {
                form = this.forms[key]
                if (form) {
                    current_key = key
                    break
                }
            }

            // console.log("formRef", formRef)
            if (!form || !form.rows || form.rows.length == 0) {
                return this.$message.error('表单不存在')
            }

            this.isFormsActiveMapping[current_key] = true
            this.fromActionsMapping[current_key] = action

            this.$nextTick(() => {
                formRef = this.$refs[current_key][0] || this.$refs[current_key]
                formRef?.edit && formRef?.edit(row)
            })
        },
        handleRowActionApi(row, action) {
            let { api_key, param_keys, method } = action
            if (api_key) {
                let params = {}

                if (param_keys) {
                    for (let item of param_keys) {
                        let [k,] = Object.keys(item)
                        let v = row[item[k]]
                        params[k] = v
                    }
                }
                console.log(this.api)
                let url = this.api[api_key]
                if (!url) throw new Error('api_key not found')
                request.post(url, params).then(res => {
                    if (res.data?.code == 200) {
                        this.load()
                    }
                })
            }
        },
        handleFormSubmit(e, form = {}) {
            console.log(e, form)
            let action = this.fromActionsMapping[form.prop] || {}
            let { api_key } = action
            let { submit_api } = form
            let api_url = submit_api || this.api[api_key]
            console.log(api_key, api_url)
            if (!api_url) throw new Error('api_key not found')

            request.post(api_url, e).then(res => {
                if (res.data?.code == 200) {
                    this.load()
                    this.isFormsActiveMapping[form.prop] = false
                }
            })
        },
        submitSearch() {
            console.log(this.searchForm)
            this.load()
        },
        resetSearchForm() {
            this.searchForm = {}
            this.load()
            // reset table sort
            this.$refs.tableRef.clearSort()
            // url 
            this.$router.push({
                query: {}
            })
        },
        handlePageSizeChange(val) {
            this.pagination.pageSize = val
            this.load()
        },
        handleCurrentPageChange(val) {
            this.pagination.currentPage = val
            this.load()
        },
        getSearchForm() {
            let form = { ...this.searchForm }
            for (let key in form) {
                if (form[key] == "") {
                    delete form[key]
                }
            }
            return form
        },
        load() {
            this.loading = true
            request({
                url: this.api.list,
                method: 'get',
                params: {
                    page: this.pagination.currentPage,
                    size: this.pagination.pageSize,
                    ...this.getSearchForm()
                }
            }).then(res => {
                let data = res.data.data || {}
                this.tableData = data?.list || []
                let { size, page, total } = data?.pageable
                this.pagination = {
                    pageSize: size,
                    currentPage: page,
                    total
                }

            }).finally(() => {
                setTimeout(() => {
                    this.loading = false
                }, 200)
            })
        },
        handleSortChange({ column, order }) {
            if (!order) return
            this.searchForm.order_by = column.rawColumnKey + (order === 'ascending' ? '__asc' : '__desc')
            this.load()
        },
        getTableSelection() {
            return this.$refs.tableRef?.getSelectionRows() || []
        },
        getTableSelectionIds() {
            return this.getTableSelection().map(item => item.id)
        },
        exportData() {
            this.$confirm('确定导出当前数据吗？', '提示', {
                confirmButtonText: this.$t("export"),
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.exportDataApi()
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消导出'
                });
            });
        },
        exportDataApi() {
            request({
                url: this.api.export,
                method: 'get',
                responseType: 'blob',
                params: {
                    ...this.getSearchForm()
                },
                binary: true
            }).then(res => {
                let blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
                let url = window.URL.createObjectURL(blob)
                let link = document.createElement('a')
                let headers = res.headers

                link.style.display = 'none'
                link.href = url
                let filename = `${this.meta.title}-导出-${this.$dayjs().format('YYYYMMDDHHmmss')}`
                link.setAttribute('download', decodeURI(filename))
                document.body.appendChild(link)
                link.click()
                document.body.removeChild(link)
                window.URL.revokeObjectURL(url)
            })
        },
        makeUrl(row, column, key) {
            let url = column.props?.url_prefix || ""
            return url + row[key]
        },
        handleQueryToSearchForm(query) {
            let flatFields = this.searchFormFields.reduce((acc, cur) => acc.concat(cur), [])
            console.log(flatFields)
            for (let key in query) {
                if (flatFields.find(v => v.prop === key)) {
                    this.searchForm[key] = query[key]
                }
            }
            this.load()
        }
    },
    created() { },
    mounted() {
        this.handleQueryToSearchForm(this.$route.query)
        this.load()
    }
};
</script>
<style lang="scss" scoped></style>