import {useApiGetters} from "../api/apiGetters.js";
import {usePhotosStore} from "./photos.js";
import {defineStore} from 'pinia'

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
    const staffDeleting = ref(false)
    const staffSnapshot = ref(new Map())
    const adminError = ref('')
    const adminSuccess = ref('')
    const {
        fetchAllStaff,
        apiAddStaff,
        apiChangeStaff,
        apiDeleteStaff,
    } = useApiGetters()

    const photosStore = usePhotosStore();

    function getApiErrorMessage(e) {
        console.log('API error:', e)

        if (
            e.code === 'ECONNABORTED' ||
            e.code === 'ERR_NETWORK' ||
            e.message === 'Network Error' ||
            !e.response
        ) {
            return 'Сервер недоступен, попробуйте позже'
        }

        const detail = e.response?.data?.detail

        if (typeof detail === 'string') {
            return detail
        }

        if (typeof detail === 'object' && detail?.message) {
            return detail.message
        }

        return 'Произошла ошибка'
    }

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
        adminError.value = ''
        adminSuccess.value = ''

        try {
            const updatedPhotos = await photosStore.uploadPhotos('staff')

            if (updatedPhotos) {
                const updatedPhotosMap = new Map(
                    updatedPhotos.map(item => [item.id, item.img_url])
                )

                allStaff.value.forEach(staff => {
                    const newUrl = updatedPhotosMap.get(staff.staff_id)
                    if (newUrl) {
                        staff.img_url = newUrl
                    }
                })
            }

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

            console.log(newItems);

            if (!newItems.length && !changedItems.length) return;

            const results = await Promise.all([
                newItems.length ? apiAddStaff(newItems) : Promise.resolve(),
                changedItems.length ? apiChangeStaff(changedItems) : Promise.resolve()
            ])

            await loadStaff();
            adminSuccess.value = 'Сохранено'
        } catch (e) {
            adminError.value = getApiErrorMessage(e);
        } finally {
            uploadingStaff.value = false
        }
    }

    async function deleteStaff(id) {
        staffDeleting.value = true

        try {
            await apiDeleteStaff({staff_id: id})
            await loadStaff()
            adminSuccess.value = 'Удалено'
        } catch (e) {
            adminError.value = getApiErrorMessage(e);
        } finally {
            staffDeleting.value = false
        }
    }

    return {
        loadingStaff,
        uploadingStaff,
        staffDeleting,
        allStaff,
        adminError,
        adminSuccess,
        loadStaff,
        uploadStaff,
        deleteStaff,
    }
})