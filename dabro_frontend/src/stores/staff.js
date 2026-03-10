import {defineStore} from "pinia";
import {ref} from "vue";
import {apiAddStaff, apiDeleteStaff, apiChangeStaff, fetchAllStaff} from "@/api/apiGetters.js";
import {usePhotosStore} from "@/stores/photos.js";

const PATCH_FIELDS = ["name", "grade", "description", "img_url"];

function toAddPayload(m) {
    return {
        name: m.name,
        grade: m.grade,
        description: m.description,
        img_url: m.img_url,
    };
}

function toPatchPayload(oldData, newData) {

    const patch = {staff_id: newData.staff_id};

    for (const field of PATCH_FIELDS) {
        if (oldData[field] !== newData[field]) {
            patch[field] = newData[field];
        }
    }

    return Object.keys(patch).length > 1 ? patch : null;
}

export const useStaffStore = defineStore('staff', () => {
    const allStaff = ref([])
    const loadingStaff = ref(false)
    const uploadingStaff = ref(false)
    const staffSnapshot = ref(new Map())

    const photosStore = usePhotosStore();

    async function loadStaff() {
        loadingStaff.value = true;
        try {
            const res = await fetchAllStaff();
            allStaff.value = res.data;

            const map = new Map()
            for (const item of res.data) {
                map.set(item.staff_id, {
                    name: item.name ?? "",
                    grade: item.grade ?? "",
                    description: item.description ?? "",
                    img_url: item.img_url ?? null,
                })
            }
            staffSnapshot.value = map;
        } catch (error) {
            console.log(error)
        } finally {
            loadingStaff.value = false;
        }
    }

    async function uploadStaff() {
        uploadingStaff.value = true

        try {
            const updatedPhotos = await photosStore.uploadPhotos('staff')
            if (!updatedPhotos) return;

            const updatedPhotosMap = new Map(
                updatedPhotos.map(item => [item.id, item.img_url])
            )

            allStaff.value.forEach(product => {
                const newUrl = updatedPhotosMap.get(product.id)
                if (newUrl) {
                    product.img_url = newUrl
                }
            })

            const newItems = [];
            const changedItems = [];

            for (const item of allStaff.value) {
                const oldData = staffSnapshot.value.get(item.staff_id)

                if (!oldData) {
                    newItems.push(toAddPayload(item));
                    continue;
                }

                const patch = toPatchPayload(oldData, item)
                if (patch) changedItems.push(patch)
            }

            if (!newItems.length && !changedItems.length) return;

            const results = await Promise.all([
                newItems.length ? apiAddStaff(newItems) : Promise.resolve(),
                changedItems.length ? apiChangeStaff(changedItems) : Promise.resolve()
            ])

            await loadStaff();
        } catch (e) {
            console.log(e);
        } finally {
            uploadingStaff.value = false
        }
    }

    async function deleteStaff(id) {
        try {
            await apiDeleteStaff({ staff_id: id })
            await loadStaff()
        } catch (e) {
            console.log(e);
        }
    }

    return {
        loadingStaff,
        uploadingStaff,
        allStaff,
        loadStaff,
        uploadStaff,
        deleteStaff,
    }
})