<template>
  <a-layout>
    <a-layout-header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="color: #fff; font-size: 1.5rem">Completed Tasks</div>
        <router-link to="/dashboard"><a-button>Back to Dashboard</a-button></router-link>
      </div>
    </a-layout-header>
    <a-layout-content :style="{ padding: '0 50px', marginTop: '24px' }">
      <a-row>
        <a-col :span="24">
          <a-list :data-source="tasks" bordered>
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta :title="item.content" />
                <div>
                  <a-tag color="blue">{{ capitalize(item.priority) }}</a-tag>
                  <span style="margin-left: 10px">{{ displayDate(item.created_at) }}</span>
                </div>
              </a-list-item>
            </template>
          </a-list>
        </a-col>
      </a-row>
      <a-empty v-if="!loading && tasks.length === 0" description="No completed tasks" style="margin-top:40px" />
    </a-layout-content>
  </a-layout>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
const tasks = ref([]);
const loading = ref(true);
const router = useRouter();
function capitalize(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}
function displayDate(val) {
  return new Date(val).toLocaleString();
}
onMounted(async () => {
  loading.value = true;
  const token = localStorage.getItem('token');
  if (!token) return router.push('/login');
  const res = await fetch('http://localhost:8000/todos?completed=true', { headers: { Authorization: `Bearer ${token}` } });
  if (res.ok) {
    tasks.value = await res.json();
  } else {
    tasks.value = [];
  }
  loading.value = false;
});
</script>
