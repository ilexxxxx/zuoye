import { reactive, computed } from 'vue'
import api from '@/api'

export const authUser = reactive({
  // 初始值先放空，会触发骨架屏或默认头像
  id: 0,
  username: '',
  fetch() {                       // ① 拉取当前登录用户
    return api.get('/users/me/').then(({ data }) => {
      Object.assign(authUser, data)   // ② 整包替换，保持响应式
    })
  },
  logout() {
    Object.assign(authUser, { id: 0, username: '' })
  }
})

// 派生头像，只要 username 一变就自动更新
export const avatarUrl = computed(() =>
  authUser.username
    ? `https://ui-avatars.com/api/?name=${encodeURIComponent(
        authUser.username.substring(0, 1).toUpperCase()
      )}&background=409eff&color=fff`
    : ''
)