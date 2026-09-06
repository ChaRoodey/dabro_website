export const useSidebarStore = defineStore('booking', () => {
    const {goToSection} = useSectionNavigation()

    const isSidebarOpen = ref(false)
    const isMobileMenuOpened = ref(false)
    const sidebarUrl = ref('')

    function openSidebar(url) {
        isSidebarOpen.value = true
        sidebarUrl.value = url

        stopLenis()
        document.body.style.overflow = "hidden"
    }

    function openBookingSidebar() {
        openSidebar('https://b921434.yclients.com/')
    }

    function openCertsSidebar() {
        openSidebar('https://o18042.yclients.com/')
    }


    function closeSidebar() {
        isSidebarOpen.value = false

        document.body.style.overflow = ""
        startLenis()
    }

    function openMobileSidebar() {
        isMobileMenuOpened.value = true;
    }

    function closeMobileSidebar(option) {
        isMobileMenuOpened.value = false;
        if (option) goToSection(option)
    }

    return {
        isMobileMenuOpened,
        isSidebarOpen,
        sidebarUrl,
        openBookingSidebar,
        openCertsSidebar,
        closeSidebar,
        openMobileSidebar,
        closeMobileSidebar,
    }
})