<template>
  <div class="detail-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration"></div>

    <el-card shadow="hover" class="meeting-card">
      <template #header>
        <div class="header-content">
          <div class="title-section">
            <div class="meeting-icon">
              <el-icon><Calendar /></el-icon>
            </div>
            <div>
              <h1 class="meeting-title">{{ meeting.title }}</h1>
              <div class="meeting-meta">
                <el-tag :type="meeting.status === 'cancelled' ? 'danger' : 'success'" size="small" class="status-tag">
                  {{ meeting.status === 'cancelled' ? '已取消' : '进行中' }}
                </el-tag>
                <span class="meta-text">创建于 {{ formatCreateTime(meeting.created_at) }}</span>
              </div>
            </div>
          </div>
          <el-button type="primary" link @click="$router.back()" class="back-btn">
            <el-icon><ArrowLeft /></el-icon>
            返回列表
          </el-button>
        </div>
      </template>

      <!-- 核心信息卡片 -->
      <div class="info-grid">
        <div class="info-card">
          <div class="info-icon time">
            <el-icon><Clock /></el-icon>
          </div>
          <div class="info-content">
            <div class="info-label">开始时间</div>
            <div class="info-value">{{ fmt(meeting.start_time) }}</div>
          </div>
        </div>

        <div class="info-card">
          <div class="info-icon time">
            <el-icon><Clock /></el-icon>
          </div>
          <div class="info-content">
            <div class="info-label">结束时间</div>
            <div class="info-value">{{ fmt(meeting.end_time) }}</div>
          </div>
        </div>

        <div class="info-card">
          <div class="info-icon location">
            <el-icon><Location /></el-icon>
          </div>
          <div class="info-content">
            <div class="info-label">会议地点</div>
            <div class="info-value">
              <el-tag v-if="meeting.room_name" type="info" size="small" class="room-tag">
                {{ meeting.room_name }}
              </el-tag>
              <span v-else class="no-room">未指定会议室</span>
            </div>
          </div>
        </div>

        <div class="info-card">
          <div class="info-icon participants">
            <el-icon><User /></el-icon>
          </div>
          <div class="info-content">
            <div class="info-label">参会人数</div>
            <div class="info-value">{{ meeting.participants?.length || 0 }} 人</div>
          </div>
        </div>
      </div>

      <!-- 会议描述 -->
      <div class="content-section">
        <div class="section-header">
          <el-icon><Document /></el-icon>
          <span class="section-title">会议描述</span>
        </div>
        <div class="description-content" :class="{ empty: !meeting.description }">
          {{ meeting.description || '暂无会议描述' }}
        </div>
      </div>

      <!-- 参会人员 -->
      <div class="participants-section">
        <div class="section-header">
          <el-icon><User /></el-icon>
          <span class="section-title">参会人员</span>
          <span class="participant-count">({{ meeting.participants?.length || 0 }})</span>
        </div>
        <div v-if="meeting.participants?.length" class="participants-grid">
          <div
            v-for="u in meeting.participants"
            :key="u.id"
            class="participant-card"
            :class="{ important: isImportantParticipant(u.id) }"
          >
            <div class="participant-avatar">
              {{ u.username.charAt(0) }}
            </div>
            <div class="participant-info">
              <div class="participant-name">{{ u.username }}</div>
              <div class="participant-role">
                <el-tag v-if="isImportantParticipant(u.id)" type="warning" size="small">重要参会人</el-tag>
                <el-tag v-else type="info" size="small">参会人</el-tag>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <el-icon><User /></el-icon>
          <p>暂无参会人员</p>
        </div>
      </div>

      <!-- 重要参会人员 -->
      <div v-if="meeting.important_participants?.length" class="important-section">
        <div class="section-header">
          <el-icon><StarFilled /></el-icon>
          <span class="section-title">重要参会人员</span>
          <span class="participant-count">({{ meeting.important_participants?.length || 0 }})</span>
        </div>
        <div class="important-grid">
          <div
            v-for="u in meeting.important_participants"
            :key="u.id"
            class="important-card"
          >
            <div class="important-avatar">
              <el-icon><StarFilled /></el-icon>
            </div>
            <div class="important-info">
              <div class="important-name">{{ u.username }}</div>
              <div class="important-badge">重要参会人</div>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'
import {
  Calendar,
  ArrowLeft,
  Clock,
  Location,
  User,
  Document,
  StarFilled
} from '@element-plus/icons-vue'

const route = useRoute()
const meeting = ref({})

onMounted(async () => {
  const { data } = await api.get(`/meetings/${route.params.id}/`)
  meeting.value = data
})

// 简单格式化日期
function fmt(dt) {
  return new Date(dt).toLocaleString('zh-CN', { hour12: false })
}

// 格式化创建时间
function formatCreateTime(dt) {
  if (!dt) return ''
  return new Date(dt).toLocaleDateString('zh-CN')
}

// 检查是否为重要参会人员
const isImportantParticipant = computed(() => (userId) => {
  return meeting.value.important_participants?.some(p => p.id === userId) || false
})
</script>

<style scoped>
.detail-container {
  min-height: 100vh;
  padding: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
}

.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%);
  pointer-events: none;
}

.meeting-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* 头部样式 */
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 8px 0;
}

.title-section {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.meeting-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.meeting-title {
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.meeting-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-tag {
  font-weight: 600;
}

.meta-text {
  color: #909399;
  font-size: 14px;
}

.back-btn {
  color: #667eea;
  font-weight: 500;
  padding: 8px 16px;
}

/* 信息网格 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.info-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.8);
}

.info-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
}

.info-icon.time {
  background: linear-gradient(135deg, #ff6b6b, #ffa500);
}

.info-icon.location {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
}

.info-icon.participants {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.info-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 4px;
}

.info-value {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.room-tag {
  font-weight: 500;
}

.no-room {
  color: #c0c4cc;
  font-style: italic;
}

/* 内容区域 */
.content-section,
.participants-section,
.important-section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid rgba(102, 126, 234, 0.1);
}

.section-header .el-icon {
  color: #667eea;
  font-size: 18px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.participant-count {
  color: #909399;
  font-size: 14px;
  font-weight: normal;
}

.description-content {
  background: rgba(102, 126, 234, 0.05);
  padding: 20px;
  border-radius: 12px;
  line-height: 1.6;
  color: #5a6270;
  border-left: 4px solid #667eea;
}

.description-content.empty {
  color: #909399;
  font-style: italic;
  background: rgba(144, 147, 153, 0.05);
  border-left-color: #c0c4cc;
}

/* 参会人员网格 */
.participants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.participant-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.participant-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.participant-card.important {
  background: rgba(255, 193, 7, 0.1);
  border-color: rgba(255, 193, 7, 0.2);
}

.participant-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 16px;
}

.participant-card.important .participant-avatar {
  background: linear-gradient(135deg, #ffa500, #ff6b6b);
}

.participant-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.participant-role {
  font-size: 12px;
}

/* 重要参会人员 */
.important-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.important-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 165, 0, 0.1));
  border-radius: 12px;
  border: 1px solid rgba(255, 193, 7, 0.3);
  transition: all 0.3s ease;
}

.important-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 165, 0, 0.2);
}

.important-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffa500, #ff6b6b);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
}

.important-name {
  font-weight: 700;
  color: #e6a23c;
  margin-bottom: 4px;
}

.important-badge {
  font-size: 12px;
  color: #e6a23c;
  background: rgba(230, 162, 60, 0.1);
  padding: 2px 8px;
  border-radius: 10px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
  background: rgba(144, 147, 153, 0.05);
  border-radius: 12px;
  border: 1px dashed #c0c4cc;
}

.empty-state .el-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .detail-container {
    padding: 16px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .participants-grid,
  .important-grid {
    grid-template-columns: 1fr;
  }

  .meeting-title {
    font-size: 20px;
  }
}
</style>