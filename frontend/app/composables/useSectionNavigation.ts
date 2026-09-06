export function useSectionNavigation() {
    function goToSection(target: string) {
        const lenis = getLenis()
        if (!lenis) return

        lenis.scrollTo(target, { offset: -100 })
    }

    return {
        goToSection,
    }
}