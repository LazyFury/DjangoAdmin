<template>
    <div id="editor"></div>
    <div style="height: 60px;"></div>
</template>

<script>
    export default{
        prop:{
            modelValue:{
                type: String,
                default: ''
            }
        },
        data(){
            return {
                value: ''
            }
        },
        watch:{
            modelValue:{
                handler(val){
                    this.value = val
                },
                immediate: true
            },
            value:{
                handler(val){
                    this.$emit('update:modelValue', val)
                    this.$emit('change', val)
                }
            }
        },
        mounted(){
            let app = this
            var quill = new Quill('#editor', {
                theme: 'snow',
                placeholder: 'Compose an epic...',
            });
            quill.on('text-change', function(delta, oldDelta, source) {
                console.log('text-change', delta, oldDelta, source);
                app.$emit('update:modelValue', quill.root.innerHTML)
                app.$emit('change', quill.root.innerHTML)
            });
            quill.on('selection-change', function(range, oldRange, source) {
                console.log('selection-change', range, oldRange, source);
            });
            quill.on("blur", function(range, oldRange) {
                console.log("blur", range, oldRange);
            });
        },
    }
</script>