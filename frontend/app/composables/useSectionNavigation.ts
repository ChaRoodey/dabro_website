export function useSectionNavigation() {
    const router = useRouter()
    const route = useRoute()

    function goToSection(target: string) {
        if (route.name !== 'index') {
            router.push({
                name: 'index',
                query: {scroll: target.replace('#', '')}
            })
            return
        }

        const lenis = getLenis()
        if (!lenis) return

        lenis.scrollTo(target, {offset: -200})
    }

    return {
        goToSection,
    }
}
