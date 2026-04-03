import {defineStore} from "pinia";
import {ref} from "vue";
import {apiUploadProductsPhotos} from "@/api/apiGetters.js";

export const usePhotosStore = defineStore('photos', () => {
    const newPhotos = ref([])

    function addNewPhoto(photo) {
        newPhotos.value.push(photo)
    }

    async function uploadPhotos(instance) {
        try {
            const currPayloadPhotos = newPhotos.value
                .filter(photo => photo.instance === instance)
                .map(({id, file}) => ({id, file}))

            if (currPayloadPhotos.length === 0) return

            const formData = new FormData()

            const meta = currPayloadPhotos.map((item, index) => {
                formData.append('files', item.file)

                return {
                    id: item.id,
                    index: index,
                }
            })
            formData.append('meta', JSON.stringify(meta))

            const res = await apiUploadProductsPhotos(formData)

            newPhotos.value = newPhotos.value.filter(photo => photo.instance !== instance)
            return res.data.files;
        } catch (e) {
            console.log(e);
        }
    }

    return {
        newPhotos,
        addNewPhoto,
        uploadPhotos,
    }
})