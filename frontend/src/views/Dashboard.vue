<template>
  <a-layout>
    <a-layout-header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="color: #fff; font-size: 1.5rem">To-Do Dashboard</div>
        <div>
          <router-link to="/completed"><a-button type="primary">Completed Tasks</a-button></router-link>
          <a-button @click="logout" style="margin-left: 10px;">Logout</a-button>
        </div>
      </div>
    </a-layout-header>
    <a-layout-content :style="{ padding: '0 50px', marginTop: '24px' }">
      <a-row style="margin-bottom: 20px" justify="space-between">
        <a-col :span="14">
          <a-input-group compact>
            <a-input
              v-model:value="todoValue"
              placeholder="Add a new to-do..."
              style="width: 60%"
              @keydown.enter="addTodo"
            />
            <a-select v-model:value="priority" style="width: 110px">
              <a-select-option value="high">High</a-select-option>
              <a-select-option value="medium">Medium</a-select-option>
              <a-select-option value="low">Low</a-select-option>
            </a-select>
            <a-select v-model:value="status" style="width: 140px">
              <a-select-option value="not_started">Not started</a-select-option>
              <a-select-option value="in_progress">In progress</a-select-option>
              <a-select-option value="completed">Completed</a-select-option>
            </a-select>
            <a-button type="primary" @click="addTodo">Add</a-button>
          </a-input-group>
        </a-col>
      </a-row>
      <a-row :gutter="24">
        <!-- High Priority -->
        <a-col :span="8">
          <h3><a-tag color="red">High Priority</a-tag></h3>
          <a-list :data-source="filterPriority('high')" bordered>
            <template #renderItem="{ item }">
              <a-list-item>
                <div style="width:100%">
                  <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                      <span>{{ item.content }}</span>
                      <clock-circle-outlined style="margin-left: 8px" />
                      <span style="font-size:10px; color:gray; margin-left:4px">{{ displayDate(item.created_at) }}</span>
                    </div>
                    <div>
                      <a-select v-model:value="item.status" style="width:128px; margin-right:8px" @change="handleStatusChange($event, item)">
                        <a-select-option value="not_started">Not started</a-select-option>
                        <a-select-option value="in_progress">In progress</a-select-option>
                        <a-select-option value="completed">Completed</a-select-option>
                      </a-select>
                      <a-button danger type="link" @click="handleDelete(item)">
                        <delete-outlined />Delete
                      </a-button>
                    </div>
                  </div>
                </div>
              </a-list-item>
            </template>
          </a-list>
        </a-col>
        <!-- Medium Priority -->
        <a-col :span="8">
          <h3><a-tag color="orange">Medium Priority</a-tag></h3>
          <a-list :data-source="filterPriority('medium')" bordered>
            <template #renderItem="{ item }">
              <a-list-item>
                <div style="width:100%">
                  <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                      <span>{{ item.content }}</span>
                      <clock-circle-outlined style="margin-left: 8px" />
                      <span style="font-size:10px; color:gray; margin-left:4px">{{ displayDate(item.created_at) }}</span>
                    </div>
                    <div>
                      <a-select v-model:value="item.status" style="width:128px; margin-right:8px" @change="handleStatusChange($event, item)">
                        <a-select-option value="not_started">Not started</a-select-option>
                        <a-select-option value="in_progress">In progress</a-select-option>
                        <a-select-option value="completed">Completed</a-select-option>
                      </a-select>
                      <a-button danger type="link" @click="handleDelete(item)">
                        <delete-outlined />Delete
                      </a-button>
                    </div>
                  </div>
                </div>
              </a-list-item>
            </template>
          </a-list>
        </a-col>
        <!-- Low Priority -->
        <a-col :span="8">
          <h3><a-tag color="blue">Low Priority</a-tag></h3>
          <a-list :data-source="filterPriority('low')" bordered>
            <template #renderItem="{ item }">
              <a-list-item>
                <div style="width:100%">
                  <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                      <span>{{ item.content }}</span>
                      <clock-circle-outlined style="margin-left: 8px" />
                      <span style="font-size:10px; color:gray; margin-left:4px">{{ displayDate(item.created_at) }}</span>
                    </div>
                    <div>
                      <a-select v-model:value="item.status" style="width:128px; margin-right:8px" @change="handleStatusChange($event, item)">
                        <a-select-option value="not_started">Not started</a-select-option>
                        <a-select-option value="in_progress">In progress</a-select-option>
                        <a-select-option value="completed">Completed</a-select-option>
                      </a-select>
                      <a-button danger type="link" @click="handleDelete(item)">
                        <delete-outlined />Delete
                      </a-button>
                    </div>
                  </div>
                </div>
              </a-list-item>
            </template>
          </a-list>
        </a-col>
      </a-row>
    </a-layout-content>
  </a-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { DeleteOutlined, ClockCircleOutlined } from '@ant-design/icons-vue';

const todoValue = ref('');
const priority = ref('medium');
const status = ref('not_started');
const tasks = ref([]);
const router = useRouter();

async function fetchTodos() {
  const token = localStorage.getItem('token');
  if (!token) return router.push('/login');
  const res = await fetch('http://localhost:8000/todos', {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (res.ok) {
    tasks.value = await res.json();
  } else {
    tasks.value = [];
  }
}

onMounted(fetchTodos);

function filterPriority(p) {
  return tasks.value.filter(t => t.priority === p && t.status !== 'completed');
}

async function addTodo() {
  const content = todoValue.value.trim();
  if (!content) return;
  const token = localStorage.getItem('token');
  if (!token) return router.push('/login');
  const res = await fetch('http://localhost:8000/todos', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ content, priority: priority.value, status: status.value })
  });
  if (res.ok) {
    todoValue.value = '';
    fetchTodos();
  }
}

function displayDate(val) {
  return new Date(val).toLocaleString();
}

async function deleteTask(id) {
  const token = localStorage.getItem('token');
  await fetch(`http://localhost:8000/todos/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  });
  fetchTodos();
}

async function updateTask(task, key, value) {
  const token = localStorage.getItem('token');
  await fetch(`http://localhost:8000/todos/${task.id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ [key]: value })
  });
  fetchTodos();
}

function handleStatusChange(val, item) {
  updateTask(item, 'status', val);
}

function handleDelete(item) {
  deleteTask(item.id);
}

function logout() {
  localStorage.removeItem('token');
  router.push('/login');
}
</script>
