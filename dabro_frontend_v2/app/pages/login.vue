<script setup>
import {useApiGetters} from "../api/apiGetters.js";

const router = useRouter()
const {loginAdmin} = useApiGetters()

const username = ref('')
const password = ref('')
const errorMessage = ref('')

async function login() {
    if (!username.value || !password.value) {
        console.log('пустая строка');
        return;
    }
    try {
        await loginAdmin({
            'username': username.value,
            'password': password.value,
        })

        await router.push('/admin')
    } catch (e) {
        errorMessage.value = e.response?.data?.detail || "Ошибка авторизации";
    }
}
</script>

<template>
    <div class="login-wrapper">
        <form @submit.prevent="login" class="login-block">
            <h2>Авторизация</h2>
            <div class="input-wrapper">
                <h3>Логин</h3>
                <input type="text" v-model="username" placeholder="Логин" autocomplete="username">
            </div>
            <div class="input-wrapper">
                <h3>Пароль</h3>
                <input type="password" v-model="password" placeholder="Пароль" autocomplete="current-password">
            </div>
            <button class="login-btn" type="submit">Войти</button>
        </form>
    </div>

    <StatusModal
            v-if="errorMessage"
            :errorMessage="errorMessage"
    />
</template>

<style scoped>
.login-wrapper {
    position: absolute;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}

.login-block {
    width: 500px;
    height: 400px;
    border: 1px solid var(--color-gold);
    border-radius: 3px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.login-block h2 {
    font-size: 24px;
    margin-bottom: 25px;
}

.input-wrapper {
    margin-bottom: 15px;
}

.input-wrapper h3 {
    font-size: 18px;
    margin-bottom: 10px;
}

.input-wrapper input {
    color: var(--color-gold);
    border: 1px solid var(--color-light-gold);
    border-radius: 3px;
    background: transparent;
    padding: 10px 15px;
}

.login-btn {
    margin-top: 30px;
    background-color: var(--color-gold);
    color: var(--color-black);
    font-weight: 500;
    font-size: 20px;
    height: 45px;
    width: 160px;
    border: 0;
}

.login-btn:hover {
    border: var(--border-hover);
    transform: scale(1.01) translateY(-5%);
}

.login-btn:active {
    transform: translateY(1%)
}
</style>