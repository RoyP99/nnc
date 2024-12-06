<template>
    <teleport to="body">
        <transition name="fade">
            <div v-if="showModal" class="pt-5 position-fixed top-0 start-0 h-100 w-100 modalzindex" style="background-color: rgba(0, 0, 0, 0.25)">
                <div id="backdrop" @clicks="backdropClick" class="modal1-dialog h-100 overflow-auto">
                    <div class="card px-0" :class="(container == null) ? 'container' : `container-${container}`" :style="(maxwidth != null) ? `max-width: ${maxwidth}` : null">
                        <div class="card-header h2">
                            {{header}}
                            <button v-if="closeable" @click='backdropClick' @clicks='$emit("update:showModal", false)' class="btn btn-text float-end"><strong>X</strong></button>
                        </div>
                        <div class="card-body">
                            <slot></slot>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </teleport>
</template>

<script setup>
import { defineProps, ref } from 'vue';

const showModal = defineModel({required: true});

const backdropClick = (event) => {
//    console.log('click');
//    console.log(event);
//    console.log(props.closeable);
    if (props.closeable == true) {
        showModal.value = false;
    }
}

const props = 
defineProps({
    closeable: {
        type: Boolean,
        required: false,
        default: false
    },
    header: {
        type: String,
        required: false,
        default: null
    },
    container: {
        type: String,
        required: false,
        default: null
    },
    maxwidth: {
        type: String,
        required: false,
        default: null
    }
})

const isVisible = ref(false);

</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s
}
.fade-enter-from, .fade-leave-to{
  opacity: 0
}
.modalzindex {
  z-index:1030
}
</style>
