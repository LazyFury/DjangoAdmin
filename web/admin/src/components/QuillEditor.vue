<template>
    <div id="toolbar"></div>
    <div id="editor"></div>
</template>

<script>
    let quill;
    export default{
        emits: ['update:modelValue', 'change'],
        props:{
            modelValue:{
                type: String,
                default: ''
            }
        },
        data(){
            return {
                value: '',
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
            let tools = [
                ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
                ['blockquote', 'code-block'],
                [{ 'header': 1 }, { 'header': 2 }],               // custom button values
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
                [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
                [{ 'direction': 'rtl' }],                         // text direction
                [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
                [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
                [{ 'font': [] }],
                [{ 'align': [] }],
                ['clean'],                                         // remove formatting button
                ['link', 'image', 'video']                         // link and image, video
        ];
            quill = new Quill('#editor', {
                theme: 'snow',
                placeholder: 'Compose an epic...',
                modules: {
                    toolbar: tools
                }
            });

            setTimeout(() => {
                quill.root.innerHTML = this.value
            }, 100);

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
        destroyed(){
            quill.root.innerHTML = ''
            quill = null
        }
    }
</script>