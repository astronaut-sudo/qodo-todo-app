<template>
  <a-row justify="center" align="middle" style="min-height:100vh">
    <a-col :span="8">
      <a-card title="Login">
        <a-form @submit.prevent="onLogin">
          <a-form-item label="Username">
            <a-input v-model:value="username" />
          </a-form-item>
          <a-form-item label="Password">
            <a-input type="password" v-model:value="password" />
          </a-form-item>
          <a-form-item>
            <a-button type="primary" html-type="submit" block :loading="loading">Login</a-button>
            <router-link to="/register"><a-button type="link" block>Register</a-button></router-link>
          </a-form-item>
          <a-form-item v-if="error">
            <a-alert type="error" :message="error" show-icon />
          </a-form-item>
        </a-form>
      </a-card>
    </a-col>
  </a-row>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);
const router = useRouter();

const onLogin = async () => {
  error.value = '';
  loading.value = true;
  try {
    const res = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: username.value, password: password.value })
    });
    if (!res.ok) throw new Error('Invalid credentials');
    const data = await res.json();
    localStorage.setItem('token', data.access_token);
    router.push('/dashboard');
  } catch (e) {
    error.value = e.message;
  }
  loading.value = false;
};
</script>
