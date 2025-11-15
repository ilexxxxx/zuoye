<template>
  <div class="dashboard">
    <!-- 顶部栏 -->
    <header class="topbar">
      <div class="logo-section">
        <div class="logo">MeetingHub</div>
        <div class="logo-subtitle">智能会议管理系统</div>
      </div>
      <el-dropdown @command="handleCommand" trigger="click">
        <span class="user">
          <el-avatar size="small" :src="avatarUrl" class="user-avatar" />
          <span class="name">{{ authUser.username }}</span>
          <el-icon class="el-icon--right"><arrow-down /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">
              <el-icon><User /></el-icon>
              个人资料
            </el-dropdown-item>
            <el-dropdown-item command="settings">
              <el-icon><Setting /></el-icon>
              设置
            </el-dropdown-item>
            <el-dropdown-item divided command="logout">
              <el-icon><SwitchButton /></el-icon>
              登出
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </header>

    <!-- 三栏主体 -->
    <main class="main">
      <div class="col" v-for="c in cards" :key="c.title">
        <el-card shadow="hover" class="glass-card" :class="`card-${c.key}`">
          <template #header>
            <div class="card-head">
              <div class="head-title">
                <div class="card-icon">
                  <el-icon v-if="c.key === 'create'"><Calendar /></el-icon>
                  <el-icon v-if="c.key === 'notify'"><Bell /></el-icon>
                  <el-icon v-if="c.key === 'meetings'"><List /></el-icon>
                </div>
                <span class="title-text">{{ c.title }}</span>
              </div>
              <el-button v-if="c.extra" link @click="c.extra.click" class="extra-btn">
                {{ c.extra.text }}
              </el-button>
            </div>
          </template>

          <!-- 1. 创建会议 -->
          <div v-if="c.key==='create'" class="card-content">
            <el-form @submit.prevent="createMeeting" label-position="top" class="meeting-form">
              <el-form-item label="会议室" class="form-item-enhanced">
                <el-select v-model="roomId" placeholder="选择会议室" filterable class="enhanced-select">
                  <el-option
                    v-for="r in rooms"
                    :key="r.id"
                    :label="`${r.name}（容量${r.capacity}）`"
                    :value="r.id"
                  />
                </el-select>
              </el-form-item>

              <el-form-item label="标题" class="form-item-enhanced">
                <el-input v-model="title" placeholder="请输入会议标题" class="enhanced-input" />
              </el-form-item>

              <el-form-item label="描述" class="form-item-enhanced">
                <el-input v-model="description" type="textarea" :rows="2" placeholder="请输入会议描述" class="enhanced-textarea" />
              </el-form-item>

              <div class="time-row">
                <el-form-item label="开始时间" class="form-item-enhanced time-item">
                  <el-date-picker
                    v-model="start_time"
                    type="datetime"
                    placeholder="选择开始时间"
                    class="enhanced-datepicker"
                  />
                </el-form-item>
                <el-form-item label="结束时间" class="form-item-enhanced time-item">
                  <el-date-picker
                    v-model="end_time"
                    type="datetime"
                    placeholder="选择结束时间"
                    class="enhanced-datepicker"
                  />
                </el-form-item>
              </div>

              <!-- 参会人员 -->
              <el-form-item label="参会人员" class="form-item-enhanced">
                <div class="participant-section">
                  <el-button @click="openSelectUser" class="select-user-btn">
                    <el-icon><User /></el-icon>
                    选择人员
                  </el-button>
                  <div class="tags-container">
                    <el-tag
                      v-for="u in selectedUsers"
                      :key="u.id"
                      closable
                      @close="toggleUser(u)"
                      :type="importantIds.includes(u.id) ? 'warning' : 'info'"
                      class="user-tag"
                    >

                      {{ u.username }}
                      <el-icon
                        style="margin-left:6px;cursor:pointer;"
                        @click.stop="toggleImportant(u)"
                      >
                        <StarFilled v-if="importantIds.includes(u.id)" style="color:#ffa500" />
                        <Star v-else />
                      </el-icon>
                    </el-tag>
                  </div>
                </div>
              </el-form-item>

              <el-button type="primary" native-type="submit" class="create-btn" :disabled="!canCreate">
                创建会议
              </el-button>
            </el-form>
          </div>

          <!-- 2. 消息提醒 -->
          <div v-if="c.key==='notify'" class="card-content">
            <div v-if="notifications.length === 0" class="empty-state">
              <el-icon size="48" color="#c0c4cc"><Bell /></el-icon>
              <p>暂无新消息</p>
            </div>
            <div v-else class="notifications-list">
              <div v-for="n in notifications" :key="n.id" class="notice-item" :class="{ unread: !n.is_read }">
                <div class="notice-content">
                  <span class="notice-message">{{ n.message }}</span>
                  <div class="notice-tags">
                    <el-tag v-if="n.room" size="small" type="info">{{ n.room.name }}</el-tag>
                    <el-tag v-if="!n.is_read" size="small" type="danger" class="unread-tag">未读</el-tag>
                  </div>
                </div>
                <div class="notice-time">{{ formatTime(n.created_at) }}</div>
              </div>
            </div>
          </div>

          <!-- 3. 会议列表 -->
          <div v-if="c.key==='meetings'" class="card-content">
            <div v-if="meetings.length === 0" class="empty-state">
              <el-icon size="48" color="#c0c4cc"><List /></el-icon>
              <p>暂无会议安排</p>
            </div>
            <el-table v-else :data="meetings" stripe size="small" class="meetings-table">
              <el-table-column label="标题" min-width="120">
                <template #default="scope">
                  <el-link type="primary" @click="goDetail(scope.row.id)" class="meeting-title">
                    {{ scope.row.title }}
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column prop="start_time" label="开始" width="140" />
              <el-table-column prop="end_time" label="结束" width="140" />
              <el-table-column label="状态" width="80">
                <template #default="scope">
                  <el-tag v-if="scope.row.status==='cancelled'" type="danger" size="small">已取消</el-tag>
                  <el-tag v-else type="success" size="small">正常</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <div class="action-buttons">
                    <el-button
                      v-if="scope.row.status==='scheduled'"
                      type="danger"
                      size="small"
                      @click="toggleStatus(scope.row)"
                      class="action-btn"
                    >取消</el-button>

                    <el-button
                      v-if="scope.row.status==='cancelled'"
                      type="warning"
                      size="small"
                      @click="toggleStatus(scope.row)"
                      class="action-btn"
                    >恢复</el-button>

                    <el-button
                      v-if="scope.row.status==='cancelled'"
                      type="info"
                      size="small"
                      @click="deleteMeeting(scope.row.id)"
                      class="action-btn"
                    >删除</el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </div>
    </main>

    <!-- 选人弹窗 -->
    <el-dialog v-model="showUserDlg" title="选择参会人员" width="480px" class="user-dialog">
      <template #header>
        <div class="dialog-header">
          <el-icon><User /></el-icon>
          <span>选择参会人员</span>
        </div>
      </template>

      <!-- 全选/取消全选当前页按钮 -->
      <div class="select-all-section">
        <el-button @click="toggleSelectCurrentPage" link type="primary" class="select-page-btn">
          {{ isCurrentPageAllSelected ? '取消全选当前页' : '全选当前页' }}
        </el-button>
      </div>

      <el-scrollbar height="350px">
        <!-- 表头 -->
        <div class="user-list-header">
          <div style="width:40px;"></div>
          <div style="width:120px;">姓名</div>
          <div style="width:100px;">角色</div>
          <div style="width:120px;">操作</div>
        </div>

        <!-- 人员行 -->
        <div
          v-for="u in currentPageUsers"
          :key="u.id"
          class="user-list-item"
        >
          <!-- 参会勾选 -->
          <el-checkbox
            v-model="checkIds"
            :label="u.id"
            class="user-checkbox"
          />

          <!-- 头像和姓名 -->
          <div class="user-info">
            <span class="user-name">{{ u.username }}</span>
          </div>

          <!-- 角色 -->
          <div class="user-role">
            <span v-if="!checkIds.includes(u.id)">普通</span>
            <span v-else-if="!importantIds.includes(u.id)" class="role-normal">普通参会人</span>
            <span v-else class="role-important">重要参会人</span>
          </div>

          <!-- 重要参会人勾选（仅左侧选中时显示） -->
          <div class="user-actions">
            <el-checkbox
              v-if="checkIds.includes(u.id)"
              v-model="importantIds"
              :label="u.id"
              @click.stop
              class="important-checkbox"
            >
              重要参会人
            </el-checkbox>
          </div>
        </div>
      </el-scrollbar>

      <!-- 分页控件 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[5, 10, 20]"
          :total="allUsers.length"
          layout="prev, pager, next, sizes"
          small
          background
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showUserDlg=false" class="cancel-btn">取消</el-button>
          <el-button type="primary" @click="confirmUser" class="confirm-btn">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowDown, User, Setting, SwitchButton, Calendar, Bell, List, Star, StarFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { authUser, avatarUrl } from '@/stores/user'

const router = useRouter()

/* 表单 & 数据 */
const title = ref('')
const description = ref('')
const start_time = ref('')
const end_time = ref('')
const roomId = ref('')
const rooms = ref([])
const meetings = ref([])
const notifications = ref([])

/* 选人相关 */
const allUsers = ref([])
const showUserDlg = ref(false)
const checkIds = ref([])          // 弹窗临时勾选
const selectedUsers = ref([])     // 最终已选用户
const importantIds = ref([])      // 重要人员子集

/* 分页相关 */
const currentPage = ref(1)
const pageSize = ref(5)

// 计算当前页显示的用户
const currentPageUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return allUsers.value.slice(start, end)
})

// 判断当前页是否全选
const isCurrentPageAllSelected = computed(() => {
  if (currentPageUsers.value.length === 0) return false
  const currentPageUserIds = currentPageUsers.value.map(u => u.id)
  return currentPageUserIds.every(id => checkIds.value.includes(id))
})

const cards = computed(() => [
  { title: '创建会议', key: 'create' },
  { title: '消息提醒', key: 'notify', extra: { text: '全部标为已读', click: markAllRead } },
  { title: '会议列表', key: 'meetings' }
])

// 计算属性：是否可以创建会议
const canCreate = computed(() => {
  return title.value && roomId.value && start_time.value && end_time.value
})

onMounted(async () => {
  await loadRooms()
  await loadUsers()
  loadMeetings()
  loadNotifications()
})

async function loadRooms() {
  const { data } = await api.get('/rooms/')
  rooms.value = data
}
async function loadMeetings() {
  const { data } = await api.get('/meetings/')
  meetings.value = data
}
async function loadNotifications() {
  const { data } = await api.get('/notifications/')
  notifications.value = data
}
async function loadUsers() {
  const { data } = await api.get('/users/')
  allUsers.value = data
}

/* 选人逻辑 */
function openSelectUser() {
  checkIds.value = selectedUsers.value.map(u => u.id)
  currentPage.value = 1 // 重置到第一页
  showUserDlg.value = true
}

function confirmUser() {
  selectedUsers.value = allUsers.value.filter(u => checkIds.value.includes(u.id))
  // 重要人员若不在本次选择则自动剔除
  importantIds.value = importantIds.value.filter(id => checkIds.value.includes(id))
  showUserDlg.value = false
}

function toggleUser(u) {
  const idx = checkIds.value.indexOf(u.id)
  if (idx > -1) checkIds.value.splice(idx, 1)
  confirmUser()
}

/* 标记/取消重要人员 */
function toggleImportant(u) {
  const idx = importantIds.value.indexOf(u.id)
  if (idx > -1) importantIds.value.splice(idx, 1)
  else importantIds.value.push(u.id)
}

/* 分页相关函数 */
// 切换全选/取消全选当前页
function toggleSelectCurrentPage() {
  const currentPageUserIds = currentPageUsers.value.map(u => u.id)

  if (isCurrentPageAllSelected.value) {
    // 取消全选当前页：从已选列表中移除当前页的所有用户
    checkIds.value = checkIds.value.filter(id => !currentPageUserIds.includes(id))
  } else {
    // 全选当前页：将当前页所有用户添加到已选列表
    const newSelectedIds = [...new Set([...checkIds.value, ...currentPageUserIds])]
    checkIds.value = newSelectedIds
  }
}

// 处理页码变化
function handleCurrentChange(page) {
  currentPage.value = page
}

// 处理每页大小变化
function handleSizeChange(size) {
  pageSize.value = size
  currentPage.value = 1 // 重置到第一页
}

/* 创建会议 */
async function createMeeting() {
  const ids = selectedUsers.value.map(u => u.id)
  const importantIdsFinal = importantIds.value.filter(id => ids.includes(id))

  const { data: check } = await api.post('/check-conflict/', {
    room: roomId.value,
    start_time: start_time.value,
    end_time: end_time.value,
    participant_ids: ids
  })
  if (!check.ok) {
    ElMessage.error(check.conflicts.join('；'))
    return
  }

  await api.post('/meetings/', {
    title: title.value,
    description: description.value,
    start_time: start_time.value,
    end_time: end_time.value,
    room: roomId.value,
    participant_ids: ids,
    important_participant_ids: importantIdsFinal
  })
  ElMessage.success('创建成功')
  resetForm()
  loadMeetings()
  loadNotifications()
}

function resetForm() {
  title.value = ''
  description.value = ''
  start_time.value = ''
  end_time.value = ''
  roomId.value = ''
  selectedUsers.value = []
  importantIds.value = []
}

/* 会议操作 */
async function toggleStatus(row) {
  try {
    await api.post(`/meetings/${row.id}/cancel/`)
    ElMessage.success(row.status === 'scheduled' ? '会议已取消' : '会议已恢复')
    loadMeetings()
    loadNotifications()
  } catch {
    ElMessage.error('操作失败')
  }
}
async function deleteMeeting(id) {
  try {
    await ElMessageBox.confirm('确认删除该会议？', '提示', { type: 'warning' })
    await api.delete(`/meetings/${id}/`)
    ElMessage.success('会议已删除')
    loadMeetings()
  } catch {}
}
function goDetail(id) {
  router.push(`/meeting/${id}`)
}
async function markAllRead() {
  await api.post('/notifications/mark_all_read/')
  const unreadCount = notifications.value.filter(n => !n.is_read).length
  ElMessage.success(`已标记 ${unreadCount} 条为已读`)
  loadNotifications()
}
function handleCommand(cmd) {
  if (cmd === 'logout') {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    ElMessage.success('已登出')
    router.push('/login')
  }
}

// 格式化时间显示
function formatTime(timeString) {
  if (!timeString) return ''
  return new Date(timeString).toLocaleString('zh-CN')
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  padding: 24px;
  position: relative;
  overflow-x: hidden;
}

.dashboard::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
  pointer-events: none;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  position: relative;
  z-index: 1;
}

.logo-section {
  display: flex;
  flex-direction: column;
}

.logo {
  font-size: 28px;
  color: #fff;
  font-weight: 800;
  letter-spacing: 1px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.logo-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 2px;
  font-weight: 300;
}

.user {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #fff;
  padding: 8px 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.user:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.user-avatar {
  background: linear-gradient(45deg, #ff6b6b, #feca57);
}

.name {
  margin-left: 8px;
  margin-right: 4px;
  font-weight: 500;
}

.main {
  display: flex;
  gap: 24px;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.col {
  flex: 1;
  max-width: 480px;
  min-width: 380px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px) saturate(180%);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  overflow: hidden;
}

.glass-card:hover {
  transform: translateY(-5px);
  box-shadow:
    0 15px 40px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.card-create {
  border-top: 4px solid #667eea;
}

.card-notify {
  border-top: 4px solid #f093fb;
}

.card-meetings {
  border-top: 4px solid #4ecdc4;
}

.card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
}

.head-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.card-create .card-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.card-notify .card-icon {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.card-meetings .card-icon {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
}

.title-text {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.extra-btn {
  color: #667eea;
  font-weight: 500;
}

.card-content {
  padding: 4px 0;
}

/* 表单样式优化 */
.meeting-form {
  padding: 8px 0;
}

.form-item-enhanced {
  margin-bottom: 20px;
}

.form-item-enhanced :deep(.el-form-item__label) {
  font-weight: 600;
  color: #5a6270;
  margin-bottom: 6px;
  font-size: 14px;
}

.enhanced-select,
.enhanced-input,
.enhanced-textarea,
.enhanced-datepicker {
  width: 100%;
}

.enhanced-input :deep(.el-input__inner),
.enhanced-select :deep(.el-input__inner),
.enhanced-textarea :deep(.el-textarea__inner),
.enhanced-datepicker :deep(.el-input__inner) {
  border-radius: 12px;
  border: 1px solid #e1e5eb;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
}

.enhanced-input :deep(.el-input__inner:focus),
.enhanced-select :deep(.el-input__inner:focus),
.enhanced-textarea :deep(.el-textarea__inner:focus),
.enhanced-datepicker :deep(.el-input__inner:focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.time-row {
  display: flex;
  gap: 16px;
}

.time-item {
  flex: 1;
}

/* 参会人员选择 */
.participant-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.select-user-btn {
  align-self: flex-start;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 8px 16px;
  font-weight: 500;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  min-height: 40px;
  padding: 8px;
  border-radius: 10px;
  background: rgba(102, 126, 234, 0.05);
}

.user-tag {
  display: flex;
  align-items: center;
  padding: 6px 10px;
  border-radius: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.user-tag:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.create-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  margin-top: 16px;
  transition: all 0.3s ease;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.create-btn:disabled {
  background: #c0c4cc;
  transform: none;
  box-shadow: none;
}

/* 消息提醒样式 */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
}

.empty-state p {
  margin-top: 12px;
  font-size: 14px;
}

.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notice-item {
  padding: 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.notice-item.unread {
  background: rgba(255, 245, 245, 0.8);
  border-left: 4px solid #ff6b6b;
}

.notice-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.notice-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.notice-message {
  flex: 1;
  font-size: 14px;
  line-height: 1.4;
  color: #5a6270;
}

.notice-tags {
  display: flex;
  gap: 6px;
  margin-left: 12px;
}

.unread-tag {
  font-weight: 600;
}

.notice-time {
  font-size: 12px;
  color: #909399;
  text-align: right;
}

/* 会议列表样式 */
.meetings-table {
  border-radius: 12px;
  overflow: hidden;
}

.meetings-table :deep(.el-table__header) {
  background: rgba(102, 126, 234, 0.1);
}

.meetings-table :deep(.el-table th) {
  background: transparent;
  color: #5a6270;
  font-weight: 600;
}

.meeting-title {
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.action-btn {
  padding: 4px 8px;
  font-size: 12px;
  border-radius: 6px;
}

/* 选人弹窗样式 */
.user-dialog :deep(.el-dialog) {
  border-radius: 20px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
}

.user-dialog :deep(.el-dialog__header) {
  padding: 20px 24px 0;
  margin-right: 0;
}

.dialog-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #2c3e50;
}

/* 全选当前页按钮样式 */
.select-all-section {
  margin-bottom: 16px;
  text-align: right;
  padding: 0 24px;
}

.select-page-btn {
  font-size: 12px;
  padding: 4px 8px;
}

.user-list-header {
  display: flex;
  margin-bottom: 16px;
  padding: 0 16px;
  font-size: 14px;
  color: #909399;
  font-weight: 600;
  text-align: center;
}

.user-list-header div:first-child {
  width: 60px; /* 增加第一列宽度 */
}

.user-list-header div:nth-child(2) {
  width: 100px; /* 姓名列宽度不变 */
  margin-left: 20px; /* 给姓名列添加左边距 */
}

.user-list-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 8px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  text-align: center;
}

.user-list-item:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: translateX(4px);
}
.user-checkbox {
  width: 90px; /* 对应增加checkbox区域宽度 */
  display: flex;
  justify-content: center;
}


.user-info {
  width: 100px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: 20px; /* 这里添加间距 */
}

.user-name {
  font-weight: 500;
  color: #5a6270;
}

.user-role {
  width: 100px;
}

.role-normal {
  color: #909399;
}

.role-important {
  color: #e6a23c;
  font-weight: 500;
}

.user-actions {
  width: 120px;
  display: flex;
  justify-content: center;
}

.important-checkbox {
  margin: 0;
}

/* 分页样式 */
.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 16px;
  padding: 12px 0;
}

.pagination-section :deep(.el-pagination) {
  justify-content: center;
}

.pagination-section :deep(.el-pagination.is-background .el-pager li) {
  border-radius: 8px;
  margin: 0 2px;
}

.pagination-section :deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn,
.confirm-btn {
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: 500;
}

.confirm-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main {
    flex-direction: column;
    align-items: center;
  }

  .col {
    max-width: 100%;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }

  .time-row {
    flex-direction: column;
    gap: 0;
  }

  .user-list-header,
  .user-list-item {
    font-size: 12px;
  }
}
</style>