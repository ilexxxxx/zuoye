<template>
  <div class="login-container">
    <!-- 背景装饰元素 -->
    <div class="decoration deco-1"></div>
    <div class="decoration deco-2"></div>
    <div class="decoration deco-3"></div>
    <div class="decoration deco-4"></div>

    <div class="login-card">
      <!-- 头部品牌区域 -->
      <div class="brand-section">
        <div class="logo">
          <el-icon size="32" color="#667eea"><Calendar /></el-icon>
        </div>
        <h1 class="title">MeetingHub</h1>
        <p class="subtitle">高效会议，轻松管理</p>
      </div>

      <el-tabs v-model="activeName" stretch class="custom-tabs">
        <el-tab-pane label="登录" name="login">
          <el-form @submit.prevent="handleLogin" :model="form" :rules="rules" ref="loginForm" class="auth-form">
            <el-form-item prop="username" class="form-item-enhanced">
              <el-input
                v-model="form.username"
                placeholder="请输入用户名"
                size="large"
                class="enhanced-input"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item prop="password" class="form-item-enhanced">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请输入密码"
                size="large"
                show-password
                class="enhanced-input"
              >
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-button
              type="primary"
              size="large"
              native-type="submit"
              :loading="loading"
              class="auth-btn login-btn"
            >
              <el-icon v-if="!loading"><Right /></el-icon>
              登 录
            </el-button>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="注册" name="register">
          <el-form @submit.prevent="handleRegister" :model="form" :rules="rules" ref="regForm" class="auth-form">
            <el-form-item prop="username" class="form-item-enhanced">
              <el-input
                v-model="form.username"
                placeholder="设置用户名"
                size="large"
                class="enhanced-input"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item prop="password" class="form-item-enhanced">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="设置密码（至少6位）"
                size="large"
                show-password
                class="enhanced-input"
              >
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-button
              type="success"
              size="large"
              native-type="submit"
              :loading="loading"
              class="auth-btn register-btn"
            >
              <el-icon v-if="!loading"><Plus /></el-icon>
              注 册
            </el-button>
          </el-form>
        </el-tab-pane>
      </el-tabs>

      <!-- 底部提示 -->
      <div class="footer-tip">
        <span v-if="activeName === 'login'">还没有账号？</span>
        <span v-else>已有账号？</span>
        <el-link type="primary" @click="activeName = activeName === 'login' ? 'register' : 'login'" class="switch-link">
          {{ activeName === 'login' ? '立即注册' : '立即登录' }}
        </el-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import api from '@/api'
import router from '@/router'
import { ElMessage } from 'element-plus'
import { authUser } from '@/stores/user'
import { Calendar, User, Lock, Right, Plus } from '@element-plus/icons-vue'

const activeName = ref('login')
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, min: 6, message: '密码至少 6 位', trigger: 'blur' }]
}

async function handleLogin() {
  loading.value = true
  try {
    const { data } = await api.post('/auth/login/', form)
    localStorage.setItem('token', data.access)
    await authUser.fetch()

    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch ({ response }) {
    ElMessage.error(response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  loading.value = true
  try {
    await api.post('/auth/register/', form)
    ElMessage.success('注册成功，请登录')
    activeName.value = 'login'
    // 清空表单
    form.username = ''
    form.password = ''
  } catch ({ response }) {
    ElMessage.error(response?.data?.username || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

/* 背景装饰元素 */
.decoration {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.deco-1 {
  width: 80px;
  height: 80px;
  top: 20%;
  left: 10%;
  animation: float 6s ease-in-out infinite;
}

.deco-2 {
  width: 120px;
  height: 120px;
  bottom: 15%;
  right: 8%;
  animation: float 8s ease-in-out infinite 1s;
}

.deco-3 {
  width: 60px;
  height: 60px;
  top: 60%;
  left: 5%;
  animation: float 5s ease-in-out infinite 0.5s;
}

.deco-4 {
  width: 100px;
  height: 100px;
  top: 10%;
  right: 15%;
  animation: float 7s ease-in-out infinite 1.5s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

.login-card {
  width: 420px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow:
    0 25px 80px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

/* 品牌区域 */
.brand-section {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.title {
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #909399;
  font-size: 14px;
  margin: 0;
  font-weight: 400;
}

/* 标签页样式 */
.custom-tabs {
  margin-bottom: 24px;
}

:deep(.custom-tabs .el-tabs__header) {
  margin-bottom: 32px;
}

:deep(.custom-tabs .el-tabs__nav-wrap::after) {
  display: none;
}

:deep(.custom-tabs .el-tabs__active-bar) {
  background: linear-gradient(135deg, #667eea, #764ba2);
  height: 3px;
  border-radius: 2px;
}

:deep(.custom-tabs .el-tabs__item) {
  font-size: 16px;
  font-weight: 600;
  color: #909399;
  padding: 0 20px 16px;
  transition: all 0.3s ease;
}

:deep(.custom-tabs .el-tabs__item.is-active) {
  color: #667eea;
}

:deep(.custom-tabs .el-tabs__item:hover) {
  color: #667eea;
}

/* 表单样式 */
.auth-form {
  margin-top: 8px;
}

.form-item-enhanced {
  margin-bottom: 24px;
}

.enhanced-input :deep(.el-input__inner) {
  height: 48px;
  border-radius: 12px;
  border: 1px solid #e1e5eb;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  font-size: 14px;
  padding-left: 12px;
}

.enhanced-input :deep(.el-input__inner:focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
  background: rgba(255, 255, 255, 0.95);
}

.enhanced-input :deep(.el-input__prefix) {
  display: flex;
  align-items: center;
  padding-left: 12px;
  color: #909399;
}

.enhanced-input:focus-within :deep(.el-input__prefix) {
  color: #667eea;
}

/* 按钮样式 */
.auth-btn {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  margin-top: 8px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.register-btn {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
  box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
}

.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(78, 205, 196, 0.4);
}

/* 底部提示 */
.footer-tip {
  text-align: center;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  color: #909399;
  font-size: 14px;
}

.switch-link {
  margin-left: 4px;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-container {
    padding: 20px;
  }

  .login-card {
    width: 100%;
    padding: 40px 24px;
  }

  .decoration {
    display: none;
  }
}

/* 加载状态 */
:deep(.el-button.is-loading) {
  opacity: 0.8;
  transform: none !important;
}
</style>